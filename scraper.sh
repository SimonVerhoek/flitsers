#!/bin/bash
set -e
source $HOME/.bash_profile

# local development
# echo 'Starting Tor...'
# tor > /dev/null &
# sleep 10

# echo 'Starting scraper...'
# python scraper.py

# echo 'Killing Tor...'
# kill $(lsof -t -i:9050)



# production
echo 'Starting scraper...'
python ~/flitsers/scraper.py
