# Production setup

The application is hosted via a systemd service, with nginx as a reverse proxy in front.

- Service config: `/etc/systemd/system/flitserdata.service`
- Working directory: `/home/administrator/flitsers`
- Venv: `/home/administrator/flitsers/venv`
- App served via Unix socket: `/home/administrator/flitsers/flitserdata.sock`

## Deploying updates

```bash
cd /home/administrator/flitsers
git pull
sudo systemctl restart flitserdata
```

## Updating the app server (Flask → FastAPI migration)

The app was migrated from Flask (WSGI) to FastAPI (ASGI). The server needs to switch from Gunicorn to Uvicorn.

**1. Install uvicorn in the venv**
```bash
cd /home/administrator/flitsers
venv/bin/pip install fastapi uvicorn
```

**2. Update `/etc/systemd/system/flitserdata.service`**

Change the `ExecStart` line:
```ini
# Before
ExecStart=/home/administrator/flitsers/venv/bin/gunicorn --workers 3 --bind unix:flitserdata.sock -m 007 wsgi:app

# After
ExecStart=/home/administrator/flitsers/venv/bin/uvicorn app.app:app --workers 3 --uds /home/administrator/flitsers/flitserdata.sock
```

**3. Reload and restart**
```bash
sudo systemctl daemon-reload
sudo systemctl restart flitserdata
sudo systemctl status flitserdata
```