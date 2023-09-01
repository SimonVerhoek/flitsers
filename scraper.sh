#!/bin/bash
set -e
source $HOME/.profile

# local development
echo 'Starting Tor...'
tor > /dev/null &
sleep 15

# echo 'Starting scraper...'
python scraper.py

# echo 'Killing Tor...'
kill "`pidof tor`"



# production
#echo 'Starting scraper...'
#source ~/.virtualenvs/flitserdata/bin/activate
#python3.7 ~/flitsers/scraper.py
