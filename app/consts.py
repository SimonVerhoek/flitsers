from collections import namedtuple
from datetime import datetime


from environs import Env


env = Env()
env.read_env()


"""
DATABASE
"""
DATABASE_URL: str = env.str("DATABASE_URL")


"""
FLITSER MELDINGEN
"""
ANWB_API_URL = 'https://api.anwb.nl/routing/v1/incidents/incidents-desktop-light'
CONTROLE_TYPES = ['Radar', 'Laser', 'ANPR']


OPENWEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'
OPENWEATHER_APP_ID: str = env.str('OPENWEATHER_APP_ID')

VOOR_ZONSOPGANG = 'voor_zonsopgang'
NA_ZONSOPGANG = 'na_zonsopgang'
NA_ZONSONDERGANG = 'na_zonsondergang'
ZONNESTANDEN = (VOOR_ZONSOPGANG, NA_ZONSOPGANG, NA_ZONSONDERGANG)


"""
TIME SLOTS FOR GRAPHS
"""
time_format = '%H:%M:%S'
timeSlot = namedtuple('timeSlot', ('name', 'title', 'start', 'stop'))

EARLY_MORNING = timeSlot(
	name='morning', 
	title="'s ochtends vroeg", 
	start=datetime.strptime('00:00:00', time_format).time(), 
	stop=datetime.strptime('07:00:00', time_format).time()
)
MORNING_RUSH_HOUR = timeSlot(
	name='morning_rush_hour', 
	title='ochtendspits', 
	start=datetime.strptime('07:00:00', time_format).time(), 
	stop=datetime.strptime('09:30:00', time_format).time()
)
LATE_MORNING = timeSlot(
	name='late_morning', 
	title='late ochtend', 
	start=datetime.strptime('09:30:00', time_format).time(), 
	stop=datetime.strptime('13:00:00', time_format).time()
)
AFTERNOON = timeSlot(
	name='afternoon', 
	title='middag', 
	start=datetime.strptime('13:00:00', time_format).time(), 
	stop=datetime.strptime('16:30:00', time_format).time()
)
EVENING_RUSH_HOUR = timeSlot(
	name='evening_rush_hour', 
	title='avondspits', 
	start=datetime.strptime('16:30:00', time_format).time(), 
	stop=datetime.strptime('19:00:00', time_format).time()
)
LATE_EVENING = timeSlot(
	name='late_evening', 
	title='late avond', 
	start=datetime.strptime('19:00:00', time_format).time(), 
	stop=datetime.strptime('23:59:59', time_format).time()
)

TIME_SLOTS = (
	EARLY_MORNING,
	MORNING_RUSH_HOUR,
	LATE_MORNING,
	AFTERNOON,
	EVENING_RUSH_HOUR,
	LATE_EVENING,
)


"""
MAPBOX
"""
MAPBOX_ACCESS_TOKEN = env.str('MAPBOX_ACCESS_TOKEN')
