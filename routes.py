from flask import Flask, render_template

import datetime
from json import dumps

from model import db_session
from model import Melding
 
app = Flask(__name__)      
 
@app.route('/')
def home():
	s = db_session()
	data = s.query(Melding).all()

	flitsers = []
	
	for flitser in data:
		s.expunge(flitser)

		# format dates and times for jsonification
		flitser.datum = flitser.datum.isoformat()
		flitser.tijd_van_melden = flitser.tijd_van_melden.isoformat()
		if flitser.laatste_activiteit:
			flitser.laatste_activiteit = flitser.laatste_activiteit.isoformat()

		flitser = flitser.__json__()

		flitsers.append(flitser)

	return render_template('home.html', flitsers=flitsers)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime.date):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

 
if __name__ == '__main__':
	app.run(debug=True)