#!/bin/bash
set -e

echo 'Starting Tor...'
tor > /dev/null &
sleep 10

echo 'Starting scraper...'
python scraper.py

echo 'Killing Tor...'
kill $(lsof -t -i:9050)