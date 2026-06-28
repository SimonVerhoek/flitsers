#!/bin/bash
set -e
source $HOME/.profile

echo 'Starting Tor...'
tor > /dev/null &

echo 'Waiting for Tor SOCKS proxy...'
for i in $(seq 1 30); do
    nc -z 127.0.0.1 9050 2>/dev/null && break
    sleep 2
done

echo 'Starting scraper...'
source venv/bin/activate
python app/scraper.py

echo 'Killing Tor...'
kill "`pidof tor`"
