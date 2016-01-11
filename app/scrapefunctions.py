from bs4 import BeautifulSoup
import re

from consts import \
WEGNUMMER, \
ZIJDE, \
HM_PAAL, \
TYPE_CONTROLE, \
TIJD, \
DETAILS, \
LINKS, \
RECHTS, \
CONTROLE_TYPES


def get_wegnummer(melding, wegnummer_id):
	wegnummer = melding.find(WEGNUMMER['element'], {WEGNUMMER['kenmerk']:wegnummer_id}).text
	wegnummer = wegnummer.strip()
	return wegnummer


def get_zijde(melding, zijde_id):
	richting = melding.find(ZIJDE['element'], {ZIJDE['kenmerk']:zijde_id}).text
	richting = richting.strip()
	if richting == LINKS:
		return 'links'
	elif richting == RECHTS:
		return 'rechts'


def get_hm_paal(melding, hm_paal_id):
	hm_paal = melding.find(HM_PAAL['element'], {HM_PAAL['kenmerk']:hm_paal_id}).text
	hm_paal = hm_paal.strip()
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
	return tijd


def get_details(melding):
	details = melding.find(DETAILS['element'], text=re.compile(DETAILS['kenmerk']))
	details = str(details)
	start = details.find('.') + 2
	end = details.find('  ', start)
	return details[start:end]