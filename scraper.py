from bs4 import BeautifulSoup
from urllib2 import urlopen
from json import dump

from classes import Melding
from scrapefunctions import get_zijde, get_wegnummer, get_hm_paal


url = "http://flits.flitsservice.nl/meldingen/vandaag.aspx"
fileName = "export"

meldingHtmlKenmerk = {'id':'bordzondersnelheid'}


soup = BeautifulSoup(urlopen(url), "html.parser")

items = {}

meldingen = soup.find_all('div', meldingHtmlKenmerk)


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
		


	elif regionale_weg:
		soort_weg = "regionale weg"
	else:
		soort_weg = None

	# get wegnummer
	# get zijde
	# get richting
	# get hm_paal
	# get type_controle
	# get tijd
	# get details



	# melding = str(melding)
	items[str(i)] = str(melding)

	# if snelweg

# print melding

export = open(fileName + ".json", "w+")
dump(items, export, indent=4)
export.close()
