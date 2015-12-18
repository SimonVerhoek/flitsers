from bs4 import BeautifulSoup
from urllib2 import urlopen
from json import dump


url = "http://flits.flitsservice.nl/meldingen/vandaag.aspx"
fileName = "export"


soup = BeautifulSoup(urlopen(url), "html.parser")

meldingen = {}

for i, melding in enumerate(soup.find_all('div', {
		'id':'bordzondersnelheid'})):
	# melding = str(melding)
	meldingen[str(i)] = str(melding)

export = open(fileName + ".json", "w+")
dump(meldingen, export, indent=4)
export.close()