from time import strftime

datum = strftime('%d-%m-%Y')

class Melding():
	
	def __init__(self, melding_id, soort_weg, wegnummer, zijde, hm_paal, type_controle, tijd, details):
		self.id = melding_id
		self.datum = datum
		self.soort_weg = soort_weg
		self.wegnummer = wegnummer
		self.zijde = zijde
		self.hm_paal = hm_paal
		self.type_controle = type_controle
		self.tijd = tijd
		self.details = details