import os
from datetime import datetime, time, date

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from consts import ZONNESTANDEN


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class DictSerializable(object):
    def _asdict(self):
        result = dict()
        for key in self.__mapper__.c.keys():
            value = getattr(self, key)
            if isinstance(value, datetime) or isinstance(value, time) or isinstance(value, date):
                value = value.isoformat()
            result[key] = value
        return result


""" MODELS """
class Melding(db.Model, DictSerializable):
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


# create db with above classes as tables
#Base.metadata.create_all(engine)
