"""
FLITSER MELDINGEN
"""
FILENAME = "export"

MELDING_HTML_ELEMENT = 'div'
MELDING_HTML = {'id':'bordzondersnelheid'}

LINKS = 'Li'
RECHTS = 'Re'
BEIDE = '<>'

CONTROLE_TYPES = ['Radar', 'Laser', 'ANPR']

# soorten info te scrapen
WEGNUMMER = {
	'element': 'div',
	'kenmerk': 'id'
}
ZIJDE = {
	'element': 'div',
	'kenmerk': 'id'
}
HM_PAAL = {
	'element': 'div',
	'kenmerk': 'id',
}
TYPE_CONTROLE = {
	'element': 'strong',
	'kenmerk': 'Type: '
}
TIJD = {
	'element': 'strong',
	'kenmerk': 'Tijd: '
}
DETAILS = {
	'element': 'td',
	'kenmerk': 'thv hmp'
}


# soorten wegen
SNELWEG = {
	'element': 'div',
	'kenmerk': 'id',
	'soort_weg': 'snelweg',
	'wegnummer_id': 'snelwegtekst',
	'zijde_id': 'richting',
	'hm_paal_id': 'hm'
}
REGIONALE_WEG = {
	'element': 'div',
	'kenmerk': 'id',
	'soort_weg': 'nweg',
	'wegnummer_id': 'nwegtekst',
	'zijde_id': 'richting',
	'hm_paal_id': 'hm'
}

WEGTYPES = [
	SNELWEG,
	REGIONALE_WEG
]


"""
LOCATIES HECTOMETERPALEN
"""
HM_PAAL_URL = 'http://hmpaal.nl/hectometer/'
HM_PAAL_WEG_URL = 'http://hmpaal.nl/weg/'

