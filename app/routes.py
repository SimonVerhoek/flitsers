from flask import Flask, render_template

from model import db_session
from model import Melding
 
app = Flask(__name__)      
 
@app.route('/')
def home():
	s = db_session()
	data = s.query(Melding).limit(5).all()

	flitsers = []
	
	for flitser in data:
		# format dates and times for jsonification
		flitser.datum = flitser.datum.isoformat()
		flitser.tijd_van_melden = flitser.tijd_van_melden.isoformat()
		if flitser.laatste_activiteit:
			flitser.laatste_activiteit.isoformat()

		flitsers.append(flitser.__json__())

	return render_template('home.html', flitsers=flitsers)
 
if __name__ == '__main__':
	app.run(debug=True)