from urllib2 import urlopen
from datetime import datetime
from json import dump
import time

from bs4 import BeautifulSoup
import schedule

from model import *
from scrapefunctions import \
	get_zijde, \
	get_wegnummer, \
	get_hm_paal, \
	get_type_controle, \
	get_tijd, \
	get_details, \
	get_hm_paal_coordinates
from consts import FILENAME, URL, LOCAL_URL
from consts import MELDING_HTML_ELEMENT, MELDING_HTML, SNELWEG, REGIONALE_WEG


def scrape_flitsers():
	today = datetime.today().strftime('%Y-%m-%d')

	try:
		soup = BeautifulSoup(urlopen(URL), "html.parser")
		meldingen = soup.find_all(MELDING_HTML_ELEMENT, MELDING_HTML)


		for melding in meldingen:
			# move to correct element level
			melding = melding.parent
			melding = melding.parent

			# identify road type
			snelweg = melding.find(
				SNELWEG['element'], 
				{SNELWEG['kenmerk']:SNELWEG['soort_weg']}
			)
			regionale_weg = melding.find(
				REGIONALE_WEG['element'], 
				{REGIONALE_WEG['kenmerk']:REGIONALE_WEG['soort_weg']}
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

			coordinates = get_hm_paal_coordinates(melding=newMelding)
			if coordinates:
				newMelding.locatie = ','.join(coordinates)
				newMelding.locatie_lat = coordinates[0]
				newMelding.locatie_lon = coordinates[1]

			# if already in db, update laatste_activiteit
			meldingSeenBefore = Melding.query.filter_by(datum=today,
														wegnummer=wegnummer, 
														details=details).first()
			if meldingSeenBefore:
				meldingSeenBefore.laatste_activiteit = datetime.now().time()
			else:
				db.session.add(newMelding)
			db.session.commit()
	except:
		print 'scraping failed at {}'.format(datetime.today())


schedule.every(5).minutes.do(scrape_flitsers)

while True:
	schedule.run_pending()
	time.sleep(1)
