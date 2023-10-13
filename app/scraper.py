import logging
import os
import random
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from sqlalchemy.orm import Session

import db
from consts import MELDING_HTML, MELDING_HTML_ELEMENT, REGIONALE_WEG, SNELWEG
from model import Melding
from scrapefunctions import (get_details, get_hm_paal, get_hm_paal_coordinates, get_tijd,
                             get_type_controle, get_weather, get_wegnummer, get_zijde)


def get_flitsers():
    today = datetime.today().strftime('%Y-%m-%d')

    SCRAPE_URL = os.getenv('SCRAPE_URL')

    ua = UserAgent()
    user_agent = ua.random
    print(f'scraping with random user agent: {user_agent}...')

    random_seconds = random.uniform(0, 45)
    print(f'randomly wait {random_seconds} seconds before scraping...')
    time.sleep(random_seconds)

    page_obj = requests.get(SCRAPE_URL, headers={'User-Agent': user_agent})

    if 'why_captcha_detail' in page_obj.text:
        msg = f'scraping failed due to CloudFlare captcha protection: {page_obj.text}'
        logging.error(msg)
        raise ValueError(msg)
    else:
        print('page scraped successfully!')
        scrape_flitsers(page_obj=page_obj, today=today)


def scrape_flitsers(page_obj, today):
    with Session(db.engine) as ses:
        soup = BeautifulSoup(page_obj.text, 'html.parser')
        meldingen = soup.find_all(MELDING_HTML_ELEMENT, MELDING_HTML)

        print(f'{len(meldingen)} meldingen found. Processing data...')

        new_count = 0
        updated_count = 0

        for melding in meldingen:
            # move to correct element level
            melding = melding.parent
            melding = melding.parent

            # identify road type
            snelweg = melding.find(
                SNELWEG['element'],
                {SNELWEG['kenmerk']: SNELWEG['soort_weg']}
            )
            regionale_weg = melding.find(
                REGIONALE_WEG['element'],
                {REGIONALE_WEG['kenmerk']: REGIONALE_WEG['soort_weg']}
            )

            if snelweg:
                soort_weg = SNELWEG['soort_weg']
                wegnummer = get_wegnummer(melding=melding, wegnummer_id=SNELWEG['wegnummer_id'])
                zijde = get_zijde(melding=melding, zijde_id=SNELWEG['zijde_id'])
                hm_paal = get_hm_paal(melding=melding, hm_paal_id=SNELWEG['hm_paal_id'])
            elif regionale_weg:
                soort_weg = REGIONALE_WEG['soort_weg']
                wegnummer = get_wegnummer(melding=melding, wegnummer_id=REGIONALE_WEG['wegnummer_id'])
                zijde = get_zijde(melding=melding, zijde_id=REGIONALE_WEG['zijde_id'])
                hm_paal = get_hm_paal(melding=melding, hm_paal_id=REGIONALE_WEG['hm_paal_id'])
            else:
                raise ValueError('unknown road type')

            type_controle = get_type_controle(melding)
            tijd = get_tijd(melding)
            details = get_details(melding)

            new_melding = Melding()
            new_melding.soort_weg = soort_weg
            new_melding.wegnummer = wegnummer
            new_melding.zijde = zijde
            new_melding.hm_paal = hm_paal
            new_melding.type_controle = type_controle
            new_melding.tijd_van_melden = tijd
            new_melding.details = details

            # if already in db, update laatste_activiteit
            melding_seen_before = ses.query(Melding).filter_by(
                datum=today,
                wegnummer=wegnummer,
                details=details
            ).first()

            if melding_seen_before:
                melding_seen_before.laatste_activiteit = datetime.now().time()
                updated_count += 1
            else:
                coordinates = get_hm_paal_coordinates(melding=new_melding)
                if coordinates:
                    new_melding.locatie = ','.join(coordinates)
                    new_melding.locatie_lat = coordinates[0]
                    new_melding.locatie_lon = coordinates[1]

                    weather = get_weather(
                        lat=coordinates[0],
                        lon=coordinates[1],
                        time_unix=int(time.time())
                    )

                    new_melding.weer_type = weather['type']
                    new_melding.weer_beschrijving = weather['beschrijving']
                    new_melding.weer_temp = weather['temp']
                    new_melding.weer_temp_max = weather['temp_max']
                    new_melding.weer_temp_min = weather['temp_min']
                    new_melding.weer_luchtdruk_hpa = weather['luchtdruk_hpa']
                    new_melding.weer_luchtvochtigheid_procent = weather['luchtvochtigheid_procent']
                    new_melding.weer_windsnelheid_m_per_sec = weather['windsnelheid_m_per_sec']
                    new_melding.weer_windrichting_graden = weather['windrichting_graden']
                    new_melding.weer_bewolking_procent = weather['bewolking_procent']
                    new_melding.weer_regen_mm = weather['regen_mm']
                    new_melding.weer_sneeuw_mm = weather['sneeuw_mm']
                    new_melding.weer_zonnestand = weather['zonnestand']
                    new_melding.weer_locatie_naam = weather['locatie_naam']

                ses.add(new_melding)
                new_count += 1

            ses.commit()

    print(f'scraping succeeded at {datetime.today()}: '
          f'{new_count} new meldingen added, {updated_count} updated.')


if __name__ == '__main__':
    get_flitsers()
