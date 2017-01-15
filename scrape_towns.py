#!/usr/bin/python
import urllib2

from bs4 import BeautifulSoup

from model import db, Town




def scrape_town_names():
    hdr = {
        "User-Agent": "Mozilla/5.0",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    req = urllib2.Request('http://home.kpn.nl/pagklein/plaatscodes.html', headers=hdr)
    soup = BeautifulSoup(urllib2.urlopen(req), 'html.parser')

    town_elements = soup.find_all('tr')

    town_keys = ['code', 'province', 'municipality', 'name']

    for i, town_element in enumerate(town_elements):
        if i == 0:
            continue
        
        values = []
        for value in town_element.stripped_strings:
            values.append(value)     

        town = Town(
            code=values[0],
            province=values[1],
            municipality=values[2],
            name=values[3]
        )
        db.session.add(town)
        db.session.commit()

    

if __name__ == '__main__':
    scrape_town_names()