import datetime
from json import dumps

from flask import render_template
from flask.ext.heroku import Heroku

from model import *


meldingen_schema = MeldingSchema(many=True)


@app.route('/')
def home():
	data = Melding.query.all()
	flitsers = meldingen_schema.dump(data)
	
	# [0] for sending without metadata like 'errors'
	return render_template('home.html', flitsers=flitsers[0])

 
if __name__ == '__main__':
	app.debug = True
	app.run()