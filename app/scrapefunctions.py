import re
from datetime import datetime
from urllib2 import urlopen
import random

from bs4 import BeautifulSoup

from consts import \
WEGNUMMER, \
ZIJDE, \
HM_PAAL, \
TYPE_CONTROLE, \
TIJD, \
DETAILS, \
LINKS, \
RECHTS, \
BEIDE, \
CONTROLE_TYPES, \
HM_PAAL_URL, \
HM_PAAL_WEG_URL


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
	elif richting == BEIDE:
		return 'beide'


def get_hm_paal(melding, hm_paal_id):
	hm_paal = melding.find(HM_PAAL['element'], {HM_PAAL['kenmerk']:hm_paal_id}).text
	hm_paal = hm_paal.strip()
	hm_paal.replace('.', ',')
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
	tijd = datetime.strptime(tijd, '%H:%M:%S').time()
	return tijd


def get_details(melding):
	details = melding.find(DETAILS['element'], text=re.compile(DETAILS['kenmerk']))
	details = str(details)
	start = details.find('.') + 2
	end = details.find('  ', start)
	return details[start:end]


def get_hm_paal_coordinates(melding):
	if melding.zijde == LINKS:
		zijde = 'L/'
		hm_paal = zijde + melding.hm_paal
	elif melding.zijde == RECHTS:
		zijde = 'R/'
		hm_paal = zijde + melding.hm_paal
	else:
		hm_paal = melding.hm_paal

	url = HM_PAAL_URL + melding.wegnummer + '/' + hm_paal + '/'

	soup = BeautifulSoup(urlopen(url), 'html.parser')

	if soup.find('div', {'class':'maps'}):		
		coordinates = soup.find('div', {'class':'maps'}).a['href']
		start = coordinates.find('=') + 1
		return coordinates[start:]
