"""
Script for adding location coordinates to
older db entries.
"""
from sqlalchemy import *

from model import db, Melding
from scrapefunctions import get_hm_paal_coordinates


meldingWithoutCoordinates = Melding.query.filter(
    Melding.locatie == None
).all()

print meldingWithoutCoordinates

for melding in meldingWithoutCoordinates:
    coordinates = get_hm_paal_coordinates(melding=melding)
    melding.locatie = coordinates if coordinates else "onbekend"
    melding.locatie

    db.session.commit()
