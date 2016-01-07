from bs4 import BeautifulSoup
import re

from consts import *

controle_types = ["Radar"]


def get_wegnummer(melding):
	wegnummer = melding.find(WEGNUMMER['element'], {WEGNUMMER['kenmerk']:'snelwegtekst'}).text
	wegnummer = wegnummer.strip()
	return wegnummer


def get_zijde(melding):
	richting = melding.find(ZIJDE['element'], {ZIJDE['kenmerk']:'richting'}).text
	richting = richting.strip()
	if richting == 'Li':
		return 'links'
	elif richting == 'Re':
		return 'rechts'


def get_hm_paal(melding):
	hm_paal = melding.find(HM_PAAL['element'], {HM_PAAL['kenmerk']:'hm'}).text
	hm_paal = hm_paal.strip()
	return hm_paal


def get_type_controle(melding):
	parentElement = melding.find(TYPE_CONTROLE['element'], text=TYPE_CONTROLE['kenmerk']).parent
	for controle_type in controle_types:
		if controle_type in str(parentElement.contents):
			return controle_type
			break


def get_tijd(melding):
	parentElement = melding.find(TIJD['element'], text=TIJD['kenmerk']).parent
	tijd = parentElement.contents[2].strip()
	return tijd


def get_details(melding):
	details = melding.find(DETAILS['element'], text=re.compile(DETAILS['kenmerk']))
	details = str(details)
	start = details.find('.') + 2
	end = details.find('  ', start)
	return details[start:end]
	