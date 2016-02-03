"""
Script for adding location coordinates to
older db entries.
"""
from sqlalchemy import *

from model import db_session, Melding
from scrapefunctions import get_hm_paal_coordinates


s = db_session()

meldingWithoutCoordinates = s.query(Melding).filter(
		Melding.locatie == None
	).all()

for melding in meldingWithoutCoordinates:
	coordinates = get_hm_paal_coordinates(melding=melding)
	melding.locatie = coordinates if coordinates else "onbekend"
	melding.locatie

	s.commit()

s.close()