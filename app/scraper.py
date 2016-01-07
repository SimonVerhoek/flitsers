from bs4 import BeautifulSoup
from urllib2 import urlopen
from json import dump

from classes import Melding
from scrapefunctions import \
	get_zijde, \
	get_wegnummer, \
	get_hm_paal, \
	get_type_controle, \
	get_tijd, \
	get_details
from consts import MELDING_HTML_ELEMENT, MELDING_HTML



fileName = "export"
url = "http://flits.flitsservice.nl/meldingen/vandaag.aspx"
urlVoorbeeld = "file:///Users/simonprive/Dropbox/programming/projects/flitsers/flitsservice_voorbeeld.html"



soup = BeautifulSoup(urlopen(url), "html.parser")

items = {}

meldingen = soup.find_all(MELDING_HTML_ELEMENT, MELDING_HTML)


for i, melding in enumerate(meldingen):
	melding = melding.parent
	melding = melding.parent

	melding_id = i

	snelweg = melding.find('div', {'id':'snelweg'})
	regionale_weg = melding.find('div', {'id':'regionale_weg'})

	# get soort weg
	if snelweg:
		soort_weg = "snelweg"
		wegnummer = get_wegnummer(melding)
		zijde = get_zijde(melding)
		hm_paal = get_hm_paal(melding)
		type_controle = get_type_controle(melding)
		tijd = get_tijd(melding)
		details = get_details(melding)

		newMelding = Melding(
			melding_id=melding_id,
			soort_weg=soort_weg,
			wegnummer=wegnummer,
			zijde=zijde,
			hm_paal=hm_paal,
			type_controle=type_controle,
			tijd=tijd,
			details=details)

		print newMelding.__dict__

	elif regionale_weg:
		soort_weg = "regionale weg"
	else:
		soort_weg = None


	# melding = str(melding)
	items[str(i)] = str(melding)

	# if snelweg


	if 'newMelding' in locals():
		export = open(fileName + ".json", "w+")
		dump(newMelding.__dict__, export, indent=4)
		export.close()
	