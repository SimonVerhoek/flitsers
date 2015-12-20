from bs4 import BeautifulSoup
import re

controle_types = ["Radar"]


def get_wegnummer(melding):
	wegnummer = melding.find('div', {'id':'snelwegtekst'}).text
	wegnummer = wegnummer.strip()
	return wegnummer


def get_zijde(melding):
	richting = melding.find('div', {'id':'richting'}).text
	richting = richting.strip()
	if richting == 'Li':
		return 'links'
	elif richting == 'Re':
		return 'rechts'


def get_hm_paal(melding):
	hm_paal = melding.find('div', {'id':'hm'}).text
	hm_paal = hm_paal.strip()
	return hm_paal


def get_type_controle(melding):
	parentElement = melding.find('strong', text='Type: ').parent
	for controle_type in controle_types:
		if controle_type in str(parentElement.contents):
			return controle_type
			break


def get_tijd(melding):
	parentElement = melding.find('strong', text='Tijd: ').parent
	tijd = parentElement.contents[2].strip()
	return tijd


def get_details(melding):
	details = melding.find('td', text=re.compile('thv hmp'))
	details = str(details)
	start = details.find('.') + 2
	end = details.find('  ', start)
	return details[start:end]
	