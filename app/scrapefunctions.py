import os
import re
from datetime import datetime

import logging
import socks
import socket
import requests
from bs4 import BeautifulSoup

from consts import \
    WEGNUMMER, \
    ZIJDE, \
    HM_PAAL, \
    TYPE_CONTROLE, \
    TIJD, \
    DETAILS, \
    LINKS, \
    RECHTS, \
    BEIDE, \
    CONTROLE_TYPES, \
    HM_PAAL_URL, \
    OPENWEATHER_API_URL, \
    VOOR_ZONSOPGANG, \
    NA_ZONSOPGANG, \
    NA_ZONSONDERGANG


def get_wegnummer(melding, wegnummer_id):
    wegnummer = melding.find(WEGNUMMER['element'], {WEGNUMMER['kenmerk']: wegnummer_id}).text
    wegnummer = wegnummer.strip()
    return wegnummer


def get_zijde(melding, zijde_id):
    richting = melding.find(ZIJDE['element'], {ZIJDE['kenmerk']: zijde_id}).text
    richting = richting.strip()
    if richting == LINKS:
        return 'links'
    elif richting == RECHTS:
        return 'rechts'
    elif richting == BEIDE:
        return 'beide'


def get_hm_paal(melding, hm_paal_id):
    hm_paal = melding.find(HM_PAAL['element'], {HM_PAAL['kenmerk']: hm_paal_id}).text
    hm_paal = hm_paal.strip()
    hm_paal.replace('.', ',')
    return hm_paal


def get_type_controle(melding):
    parentElement = melding.find(TYPE_CONTROLE['element'], text=TYPE_CONTROLE['kenmerk']).parent
    for controle_type in CONTROLE_TYPES:
        if controle_type in str(parentElement.contents):
            return controle_type
            break


def get_tijd(melding):
    parentElement = melding.find(TIJD['element'], text=TIJD['kenmerk']).parent
    tijd = parentElement.contents[2].strip()
    tijd = datetime.strptime(tijd, '%H:%M:%S').time()
    return tijd


def get_details(melding):
    details = melding.find(DETAILS['element'], text=re.compile(DETAILS['kenmerk']))
    details = str(details)
    start = details.find('.') + 2
    end = details.find('  ', start)
    return details[start:end]


def get_hm_paal_coordinates(melding):
    if melding.zijde == LINKS:
        zijde = 'L/'
        hm_paal = zijde + melding.hm_paal
    elif melding.zijde == RECHTS:
        zijde = 'R/'
        hm_paal = zijde + melding.hm_paal
    else:
        hm_paal = melding.hm_paal

    url = HM_PAAL_URL + melding.wegnummer + '/' + hm_paal + '/'

    page = get_hm_paal_page(url)
    soup = BeautifulSoup(page.text, "html.parser")

    coordinateList = None

    if soup.find('div', {'class': 'maps'}):
        coordinates = soup.find('div', {'class': 'maps'}).a['href']
        start = coordinates.find('=') + 1
        coordinates = coordinates[start:]

        coordinateList = coordinates.split(',')

        [float(coordinate) for coordinate in coordinateList]

    return coordinateList


def get_hm_paal_page(url):
    # setup Tor
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
    socket.socket = socks.socksocket

    try:
        page = requests.get(url)
        return page
    except requests.exceptions.RequestException as e:
        msg = f'hm_paal scraping failed: {e}'
        print(msg)
        logging.error(msg)


def get_weather(lat, lon, time_unix):
    params = {
        'APPID': os.getenv('OPENWEATHER_APP_ID'),
        'units': 'metric',
        'lang': 'nl',
        'lat': lat,
        'lon': lon,
    }
    r = requests.get(OPENWEATHER_API_URL, params=params)
    data = r.json()

    # Openweather API rain & snow key seems to vary between "1h" and "3h",
    # so if it exists just get the first value found and be done with it
    rain = list(data['rain'].values())[0] if 'rain' in data else None
    snow = list(data['snow'].values())[0] if 'snow' in data else None

    zonnestand = NA_ZONSOPGANG
    if time_unix <= data['sys']['sunrise']:
        zonnestand = VOOR_ZONSOPGANG
    elif time_unix >= data['sys']['sunset']:
        zonnestand = NA_ZONSONDERGANG

    return {
        'type': data['weather'][0]['main'],
        'beschrijving': data['weather'][0]['description'],
        'temp': data['main']['temp'],
        'temp_max': data['main']['temp_max'],
        'temp_min': data['main']['temp_min'],
        'luchtdruk_hpa': data['main']['pressure'],
        'luchtvochtigheid_procent': data['main']['humidity'],
        'windsnelheid_m_per_sec': data['wind']['speed'],
        'windrichting_graden': data['wind']['deg'],
        'bewolking_procent': data['clouds']['all'],
        'regen_mm': rain,
        'sneeuw_mm': snow,
        'zonnestand': zonnestand,
        'locatie_naam': data['name'],
    }
