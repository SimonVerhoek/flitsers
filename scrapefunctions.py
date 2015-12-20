from bs4 import BeautifulSoup


def get_zijde(melding):
	richting = melding.find('div', {'id':'richting'}).text
	richting = richting.strip()
	if richting == 'Li':
		return 'links'
	elif richting == 'Re':
		return 'rechts'


def get_wegnummer(melding):
	wegnummer = melding.find('div', {'id':'snelwegtekst'}).text
	wegnummer = wegnummer.strip()
	return wegnummer


def get_hm_paal(melding):
	hm_paal = melding.find('div', {'id':'hm'}).text
	hm_paal = hm_paal.strip()
	return hm_paal