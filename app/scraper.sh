#!/bin/bash
set -e
source $HOME/.profile

echo 'Starting scraper...'
source venv/bin/activate
python app/scraper.py
