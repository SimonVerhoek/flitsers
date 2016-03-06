import datetime
from json import dumps

from flask import render_template
from flask.ext.heroku import Heroku

from model import *

melding_schema = MeldingSchema()
meldingen_schema = MeldingSchema(many=True)


@app.route('/')
def home():
	data = Melding.query.all()
	flitsers = meldingen_schema.dump(data)
	return render_template('home.html', flitsers=flitsers)

 
if __name__ == '__main__':
	app.debug = True
	app.run()