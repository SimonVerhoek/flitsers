from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from flask.ext.heroku import Heroku


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dxqgfmksnasfzc:6LuF-BmI6yFF-5ghGKeOCowmuB@ec2-107-20-242-191.compute-1.amazonaws.com:5432/d7524e3jijp1f0'
db = SQLAlchemy(app)
heroku = Heroku(app)


""" MODELS """
class Melding(db.Model):
	__tablename__ = 'melding'
	id = db.Column(db.Integer, primary_key=True, nullable=False)
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


""" SCHEMAS (for JSON-serialization) """
class MeldingSchema(Schema):
	id = fields.Integer()
	datum = fields.Date()
	soort_weg = fields.String()
	wegnummer = fields.String()
	zijde = fields.String()
	hm_paal = fields.String()
	type_controle = fields.String()
	tijd_van_melden = fields.Time()
	details = fields.String()
	laatste_activiteit = fields.DateTime()
	locatie = fields.String()
	locatie_lat = fields.Float()
	locatie_lon = fields.Float()


# create db with above classes as tables
#Base.metadata.create_all(engine)

