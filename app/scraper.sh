#!/bin/bash
set -e
source $HOME/.profile

echo 'Starting Tor...'
tor > /dev/null &
sleep 15

echo 'Starting scraper...'
source venv/bin/activate
python app/scraper.py

echo 'Killing Tor...'
kill "`pidof tor`"
