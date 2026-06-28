from model import Melding, db_session

s = db_session()

meldingen = s.query(Melding).all()

for melding in meldingen:
    if melding.locatie != "onbekend":
        coordinates = melding.locatie.split(",")
        melding.locatie_lat = float(coordinates[0])
        melding.locatie_lon = float(coordinates[1])
        s.commit()

s.close()
