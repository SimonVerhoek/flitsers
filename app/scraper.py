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
from consts import MELDING_HTML_ELEMENT, MELDING_HTML, SNELWEG, REGIONALE_WEG



fileName = "export"
url = "http://flits.flitsservice.nl/meldingen/vandaag.aspx"
urlVoorbeeld = "file:///Users/simonprive/Dropbox/programming/projects/flitsers/app/flitsservice_voorbeeld.html"



soup = BeautifulSoup(urlopen(urlVoorbeeld), "html.parser")

items = {}

meldingen = soup.find_all(MELDING_HTML_ELEMENT, MELDING_HTML)


for i, melding in enumerate(meldingen):
	melding = melding.parent
	melding = melding.parent

	snelweg = melding.find(
		SNELWEG['element'], 
		{SNELWEG['kenmerk']:SNELWEG['soort_weg']}
	)
	regionale_weg = melding.find(
		REGIONALE_WEG['element'], 
		{REGIONALE_WEG['kenmerk']:REGIONALE_WEG['soort_weg']}
	)

	# get soort weg
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
		melding_id=i,
		soort_weg=soort_weg,
		wegnummer=wegnummer,
		zijde=zijde,
		hm_paal=hm_paal,
		type_controle=type_controle,
		tijd=tijd,
		details=details
	)

	print newMelding.__dict__


	# melding = str(melding)
	items[str(i)] = str(melding)

	# if snelweg


	if 'newMelding' in locals():
		export = open(fileName + ".json", "w+")
		dump(newMelding.__dict__, export, indent=4)
		export.close()
	