"""
Script for adding location coordinates to
older db entries.
"""
from sqlalchemy import *

from model import db, Melding
from scrapefunctions import get_hm_paal_coordinates


def get_missing_coordinates():
    melding_without_coordinates = Melding.query.filter_by(locatie=None).all()

    for melding in melding_without_coordinates:
        coordinates = get_hm_paal_coordinates(melding=melding)
        melding.locatie = coordinates if coordinates else "onbekend"
        if coordinates and coordinates != 'onbekend':
            melding.locatie_lat = coordinates[0]
            melding.locatie_lon = coordinates[1]

        db.session.commit()


def retry_unknown_coordinates():
    melding_with_unknown_coordinates = Melding.query.filter_by(locatie='onbekend').all()

    for melding in melding_with_unknown_coordinates:
        coordinates = get_hm_paal_coordinates(melding=melding)

        melding.locatie = coordinates if coordinates else "onbekend"

        db.session.commit()


def retry_wrong_coordinates():
    melding_with_wrong_coordinates = Melding.query.filter(Melding.locatie.like('{%')).all()

    for melding in melding_with_wrong_coordinates:
        coordinates = melding.locatie[1:-1]
        melding.locatie = coordinates

        coordinates = coordinates.split(',')
        melding.locatie_lat = coordinates[0]
        melding.locatie_lon = coordinates[1]

        db.session.commit()


get_missing_coordinates()
