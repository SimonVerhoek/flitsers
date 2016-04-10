import datetime
from json import dumps

from flask import render_template

from model import *

# executes scraper
# import scraper


meldingen_schema = MeldingSchema(many=True)


@app.route('/')
def home():
	q = Melding.query
	data = q.all()
	flitsers = meldingen_schema.dump(data)

	first_flitser = q.order_by(Melding.datum).first()

	# [0] for sending without metadata like 'errors'
	return render_template(
		'content.html', 
		data=data, 
		first_flitser=first_flitser,
		flitsers=flitsers[0]
	)

 
if __name__ == '__main__':
	app.debug = True
	app.run()