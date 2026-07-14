# Production setup

The application is hosted via a systemd service, with nginx as a reverse proxy in front.

- Service config: `/etc/systemd/system/flitserdata.service`
- Working directory: `/home/administrator/flitserdata`
- Venv: `/home/administrator/flitserdata/venv`
- App served via Unix socket: `/home/administrator/flitserdata/flitserdata.sock`

## Fresh server setup

Use Ubuntu 22.04 LTS (jammy), 24.04 LTS (noble), or 26.04 LTS.

**Step 1 — System dependencies**
```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y git nginx postgresql postgresql-contrib \
  make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
  libsqlite3-dev curl llvm libncursesw5-dev xz-utils tk-dev \
  libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```
The extra packages are build dependencies required by pyenv to compile Python.

**Step 2 — Server hardening**

*Firewall (UFW)*
```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status
```

*Automatic security updates*
```bash
sudo apt-get install -y unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```
This enables automatic install of security patches only (not major upgrades).

*Disable root SSH login and password authentication*

Edit `/etc/ssh/sshd_config`:
```
PermitRootLogin no
PasswordAuthentication no
```

```bash
sudo systemctl restart ssh
```

> Ensure your SSH key is working before disabling password auth, or you will be locked out.

*fail2ban (brute-force protection)*
```bash
sudo apt-get install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

**Step 3 — PostgreSQL user and database**

Create the user without a password first, then set it interactively via `\password` — this
avoids the password appearing in shell history or `ps` output:
```bash
sudo -u postgres psql -c "CREATE USER administrator;"
sudo -u postgres psql -c "\password administrator"
sudo -u postgres psql -c "CREATE DATABASE flitserdata OWNER administrator;"
```

If migrating from an existing server, restore the database now:
```bash
# On the old server — dump the database
pg_dump -U administrator flitserdata > flitserdata_$(date +%Y%m%d).sql

# From your local machine, or directly between servers — transfer the dump
scp 'administrator@<old-server-ip>:~/flitserdata_*.sql' administrator@<new-server-ip>:~
# Note: single quotes prevent the local shell from expanding the glob — the remote side resolves it.
# SSH config Host aliases work too: scp 'oldserver:~/flitserdata_*.sql' newserver:~
# When run from a local machine, the local machine needs SSH key access to both servers.

# On the new server — restore
psql -U administrator -d flitserdata < ~/flitserdata_*.sql
```

Verify row counts match:
```bash
psql -U administrator -d flitserdata -c "SELECT COUNT(*) FROM melding;"
# Compare with old server output of the same query
```

**Step 4 — Python (via pyenv) + venv + Poetry**

Install pyenv:
```bash
curl https://pyenv.run | bash
```

Add to `~/.bashrc` (then `source ~/.bashrc`):
```bash
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Install Python 3.11:
```bash
pyenv install 3.11
```

The venv and Poetry install happen inside the cloned repo — see step 6.

**Step 5 — SSH deploy key**
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub
# → add this public key as a read-only Deploy Key in the repo settings on GitHub/GitLab
```

**Step 6 — Clone the repo and set up the venv**
```bash
cd /home/administrator
git clone git@github.com:<user>/<repo>.git flitserdata
cd flitserdata
```

Create the virtualenv (using standard `venv`, NOT `pyenv virtualenv`):
```bash
pyenv local 3.11       # writes .python-version; makes `python` resolve to 3.11
python -m venv venv    # creates repo-root venv using pyenv's Python 3.11
```

Install Poetry inside the venv, then install project dependencies:
```bash
venv/bin/pip install poetry
venv/bin/poetry install --only main
```

The venv lives at `/home/administrator/flitserdata/venv`. Both the scraper and the
systemd service reference it via this path.

**Step 7 — Create `.env`**

Copy `.env` from the old server (or create from scratch):
```
DATABASE_URL=postgresql://administrator:<password>@localhost:5432/flitserdata
OPENWEATHER_APP_ID=<key>
MAPBOX_ACCESS_TOKEN=<token>
```

**Step 8 — systemd service**

Create `/etc/systemd/system/flitserdata.service`:
```ini
[Unit]
Description=Flitser Data API
After=network.target

[Service]
User=administrator
Group=administrator
UMask=007
WorkingDirectory=/home/administrator/flitserdata/app
EnvironmentFile=/home/administrator/flitserdata/.env
ExecStart=/home/administrator/flitserdata/venv/bin/uvicorn app:app --workers 3 --uds /home/administrator/flitserdata/flitserdata.sock
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable flitserdata
sudo systemctl start flitserdata
```

**Step 9 — nginx**

Create `/etc/nginx/sites-available/flitserdata`:
```nginx
server {
    listen 80;
    server_name <your-domain>;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/administrator/flitserdata/flitserdata.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/flitserdata /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Step 9a — Fix Unix socket permissions**

nginx runs as `www-data` and by default cannot traverse `/home/administrator` (mode `750`)
or connect to the socket (mode `600`). Fix both:

```bash
# Allow www-data to traverse the home directory
sudo chmod o+x /home/administrator

# Add www-data to the administrator group so it can access the 770 socket
sudo usermod -aG administrator www-data

# Restart nginx to pick up the new group membership
sudo systemctl restart nginx
```

If the service was already running before applying the `UMask` fix in Step 8, restart
it to recreate the socket with the correct permissions:
```bash
sudo systemctl daemon-reload
sudo systemctl restart flitserdata
```

Verify the socket exists and has the right permissions:
```bash
ls -la /home/administrator/flitserdata/flitserdata.sock
# Expected: srwxrwx--- 1 administrator administrator ...
```

Test nginx → uvicorn connectivity directly:
```bash
sudo systemctl status flitserdata          # must be active (running)
curl -s --unix-socket /home/administrator/flitserdata/flitserdata.sock http://localhost/ | head -5
```

> **Note:** `server_name` must be set to the real domain (e.g. `flitserdata.nl`) before running certbot in the next step.

**Step 9b — TLS certificate (Let's Encrypt)**

Install certbot with the nginx plugin:
```bash
sudo apt-get install -y certbot python3-certbot-nginx
```

Obtain and install a certificate (certbot will auto-update the nginx config to add a
`listen 443 ssl` block and redirect HTTP → HTTPS):
```bash
sudo certbot --nginx -d flitserdata.nl
```

Follow the interactive prompts (enter an email for renewal notices, agree to ToS).
Certbot writes the certificate to `/etc/letsencrypt/live/flitserdata.nl/` and edits
`/etc/nginx/sites-available/flitserdata` in place.

Verify auto-renewal works:
```bash
sudo certbot renew --dry-run
```

**Step 10 — Install and enable Tor as a persistent daemon**

See [Upgrading Tor](#upgrading-tor) for installation steps. Once installed, enable it as a
persistent service so it is always ready with established circuits:

```bash
sudo systemctl enable --now tor
```

> **Note on Ubuntu 26.04:** The Tor Project repository may not yet publish packages for the
> 26.04 codename. After `apt-get update`, check for a 404 on the tor.list entry. If it fails,
> check https://deb.torproject.org/torproject.org/dists/ for the supported codenames.

**Step 11 — Cron job (scraper)**

```bash
crontab -e
```

Add:
```
*/10 * * * * cd /home/administrator/flitserdata && ./app/scraper.sh
```

## Deploying updates

```bash
cd /home/administrator/flitserdata
git pull
sudo systemctl restart flitserdata
```

## Updating the app server (Flask → FastAPI migration)

The app was migrated from Flask (WSGI) to FastAPI (ASGI). The server needs to switch from Gunicorn to Uvicorn.

**1. Install uvicorn in the venv**
```bash
cd /home/administrator/flitserdata
venv/bin/pip install fastapi uvicorn
```

**2. Update `/etc/systemd/system/flitserdata.service`**

Change the `ExecStart` line:
```ini
# Before
ExecStart=/home/administrator/flitserdata/venv/bin/gunicorn --workers 3 --bind unix:flitserdata.sock -m 007 wsgi:app

# After
ExecStart=/home/administrator/flitserdata/venv/bin/uvicorn app:app --workers 3 --uds /home/administrator/flitserdata/flitserdata.sock
```

**3. Reload and restart**
```bash
sudo systemctl daemon-reload
sudo systemctl restart flitserdata
sudo systemctl status flitserdata
```

## Upgrading Tor

> **Note:** Ubuntu 18.04 (bionic) is not supported by the Tor Project repository.
> If the server still runs bionic, provision a fresh Ubuntu 22.04+ server instead —
> see [Fresh server setup](#fresh-server-setup) above.

The default Ubuntu apt repository ships an outdated Tor version. Install from the official Tor Project repository instead:

```bash
sudo apt-get install -y curl gpg apt-transport-https

curl -fsSL https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc \
    | sudo gpg --dearmor -o /usr/share/keyrings/tor-archive-keyring.gpg

CODENAME=$(. /etc/os-release && echo "$VERSION_CODENAME")
echo "deb [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org $CODENAME main" \
    | sudo tee /etc/apt/sources.list.d/tor.list

sudo apt-get update
sudo apt-get install -y tor deb.torproject.org-keyring
```

Verify:
```bash
tor --version
```

## Completing a server migration

After restoring the database in step 3 and completing the full fresh server setup:

**Recreate the cron job**

The cron job is not stored in the repo — recreate it on the new server per step 11 of
Fresh server setup above (note the corrected path: `./app/scraper.sh`).

Disable it on the old server before (or immediately after) cutting over DNS to avoid
both servers writing to the database simultaneously:
```bash
# On old server, once new server is confirmed working:
crontab -e  # comment out or delete the scraper line
```

**Verify the app**
```bash
sudo systemctl status flitserdata
curl -s http://localhost --unix-socket /home/administrator/flitserdata/flitserdata.sock | head -20
```

**Cut over DNS**

Point your domain's A record to the new server IP. Once DNS propagates and the app is confirmed working, decommission the old server.