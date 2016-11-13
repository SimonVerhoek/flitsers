#!/bin/bash
set -e

# local development
# echo 'Starting Tor...'
# tor > /dev/null &
# sleep 10

# echo 'Starting scraper...'
# python scraper.py

# echo 'Killing Tor...'
# kill $(lsof -t -i:9050)



# production
echo 'Starting Tor...'
sudo service tor start
sleep 10

echo 'Starting scraper...'
python scraper.py

echo 'Killing Tor...'
sudo service tor stop