from model import db_session
from model import Melding

s = db_session()

meldingen = s.query(Melding).limit(5).all()

for melding in meldingen:
	coordinates = melding.locatie.split(',')
	print coordinates


print meldingen