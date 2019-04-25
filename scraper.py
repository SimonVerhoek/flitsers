import time

from bs4 import BeautifulSoup
import logging
import requests

from model import *
from scrapefunctions import \
    get_zijde, \
    get_wegnummer, \
    get_hm_paal, \
    get_type_controle, \
    get_tijd, \
    get_details, \
    get_hm_paal_coordinates, \
    get_weather
from consts import MELDING_HTML_ELEMENT, MELDING_HTML, SNELWEG, REGIONALE_WEG
from credentials import SCRAPE_URL


def get_flitsers():
    today = datetime.today().strftime('%Y-%m-%d')

    try:
        page_obj = requests.get(SCRAPE_URL)
        scrape_flitsers(page_obj=page_obj, today=today)
    except requests.exceptions.RequestException as e:
        msg = f'scraping failed at {datetime.today()}: {e}'
        print(msg)
        logging.error(msg)


def scrape_flitsers(page_obj, today):
    soup = BeautifulSoup(page_obj.text, 'html.parser')
    meldingen = soup.find_all(MELDING_HTML_ELEMENT, MELDING_HTML)

    new_meldingen = 0

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
            pass

        type_controle = get_type_controle(melding)
        tijd = get_tijd(melding)
        details = get_details(melding)

        newMelding = Melding(
            soort_weg=soort_weg,
            wegnummer=wegnummer,
            zijde=zijde,
            hm_paal=hm_paal,
            type_controle=type_controle,
            tijd_van_melden=tijd,
            details=details
        )

        # if already in db, update laatste_activiteit
        meldingSeenBefore = Melding.query.filter_by(
            datum=today,
            wegnummer=wegnummer,
            details=details
        ).first()
        if meldingSeenBefore:
            meldingSeenBefore.laatste_activiteit = datetime.now().time()
        else:
            coordinates = get_hm_paal_coordinates(melding=newMelding)
            if coordinates:
                newMelding.locatie = ','.join(coordinates)
                newMelding.locatie_lat = coordinates[0]
                newMelding.locatie_lon = coordinates[1]

                weather = get_weather(
                    lat=coordinates[0],
                    lon=coordinates[1],
                    time_unix=int(time.time())
                )

                newMelding.weer_type = weather['type']
                newMelding.weer_beschrijving = weather['beschrijving']
                newMelding.weer_temp = weather['temp']
                newMelding.weer_temp_max = weather['temp_max']
                newMelding.weer_temp_min = weather['temp_min']
                newMelding.weer_luchtdruk_hpa = weather['luchtdruk_hpa']
                newMelding.weer_luchtvochtigheid_procent = weather['luchtvochtigheid_procent']
                newMelding.weer_windsnelheid_m_per_sec = weather['windsnelheid_m_per_sec']
                newMelding.weer_windrichting_graden = weather['windrichting_graden']
                newMelding.weer_bewolking_procent = weather['bewolking_procent']
                newMelding.weer_regen_mm = weather['regen_mm']
                newMelding.weer_sneeuw_mm = weather['sneeuw_mm']
                newMelding.weer_zonnestand = weather['zonnestand']
                newMelding.weer_locatie_naam = weather['locatie_naam']

            db.session.add(newMelding)
            new_meldingen += 1
        db.session.commit()

    print('scraping succeeded at {}: {} new meldingen added'.format(datetime.today(), new_meldingen))


if __name__ == '__main__':
    get_flitsers()
