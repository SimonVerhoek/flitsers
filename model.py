import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from credentials import DATABASE_URL
from consts import ZONNESTANDEN


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)


""" MODELS """
class Melding(db.Model):
    __tablename__ = 'melding'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datum = db.Column(db.DateTime, nullable=False, default=datetime.now())
    soort_weg = db.Column(db.String, nullable=False)
    wegnummer = db.Column(db.String, nullable=False)
    zijde = db.Column(db.String, nullable=False)
    hm_paal = db.Column(db.String, nullable=False)
    type_controle = db.Column(db.String, nullable=False)
    tijd_van_melden = db.Column(db.Time, nullable=False)
    details = db.Column(db.String)
    laatste_activiteit = db.Column(db.DateTime)
    locatie = db.Column(db.String)
    locatie_lat = db.Column(db.Float)
    locatie_lon = db.Column(db.Float)
    weer_type = db.Column(db.String)
    weer_beschrijving = db.Column(db.String)
    weer_temp = db.Column(db.Float)
    weer_temp_max = db.Column(db.Float)
    weer_temp_min = db.Column(db.Float)
    weer_luchtdruk_hpa = db.Column(db.Integer)
    weer_luchtvochtigheid_procent = db.Column(db.Integer)
    weer_windsnelheid_m_per_sec = db.Column(db.Float)
    weer_windrichting_graden = db.Column(db.Integer)
    weer_bewolking_procent = db.Column(db.Integer)
    weer_regen_mm = db.Column(db.Float)
    weer_sneeuw_mm = db.Column(db.Float)
    weer_zonnestand = db.Column(db.Enum(*ZONNESTANDEN))
    weer_locatie_naam = db.Column(db.String)


class Town(db.Model):
    __tablename__ = 'town'
    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    municipality = db.Column(db.String)
    province = db.Column(db.String)


""" SCHEMAS (for JSON-serialization) """
class MeldingSchema(Schema):
    id = fields.Integer()
    datum = fields.Date()
    soort_weg = fields.String()
    wegnummer = fields.String()
    zijde = fields.String()
    hm_paal = fields.String()
    type_controle = fields.String()
    tijd_van_melden = fields.Time(format='%H-%m-%s')
    details = fields.String()
    laatste_activiteit = fields.DateTime()
    locatie = fields.String()
    locatie_lat = fields.Float()
    locatie_lon = fields.Float()
    weer_type = fields.String()
    weer_beschrijving = fields.String()
    weer_temp = fields.Float()
    weer_temp_max = fields.Float()
    weer_temp_min = fields.Float()
    weer_luchtdruk_hpa = fields.Integer()
    weer_luchtvochtigheid_procent = fields.Integer()
    weer_windsnelheid_m_per_sec = fields.Float()
    weer_windrichting_graden = fields.Integer()
    weer_bewolking_procent = fields.Integer()
    weer_regen_mm = fields.Float()
    weer_sneeuw_mm = fields.Float()
    weer_zonnestand = fields.String()
    weer_locatie_naam = fields.String()


# create db with above classes as tables
#Base.metadata.create_all(engine)
