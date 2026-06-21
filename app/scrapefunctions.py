import os
from datetime import datetime

import logging
import requests

from consts import \
    OPENWEATHER_API_URL, \
    VOOR_ZONSOPGANG, \
    NA_ZONSOPGANG, \
    NA_ZONSONDERGANG


def get_weather(lat, lon, time_unix):
    params = {
        'APPID': os.getenv('OPENWEATHER_APP_ID'),
        'units': 'metric',
        'lang': 'nl',
        'lat': lat,
        'lon': lon,
    }
    r = requests.get(OPENWEATHER_API_URL, params=params)
    data = r.json()

    # Openweather API rain & snow key seems to vary between "1h" and "3h",
    # so if it exists just get the first value found and be done with it
    rain = list(data['rain'].values())[0] if 'rain' in data else None
    snow = list(data['snow'].values())[0] if 'snow' in data else None

    zonnestand = NA_ZONSOPGANG
    if time_unix <= data['sys']['sunrise']:
        zonnestand = VOOR_ZONSOPGANG
    elif time_unix >= data['sys']['sunset']:
        zonnestand = NA_ZONSONDERGANG

    return {
        'type': data['weather'][0]['main'],
        'beschrijving': data['weather'][0]['description'],
        'temp': data['main']['temp'],
        'temp_max': data['main']['temp_max'],
        'temp_min': data['main']['temp_min'],
        'luchtdruk_hpa': data['main']['pressure'],
        'luchtvochtigheid_procent': data['main']['humidity'],
        'windsnelheid_m_per_sec': data['wind']['speed'],
        'windrichting_graden': data['wind']['deg'],
        'bewolking_procent': data['clouds']['all'],
        'regen_mm': rain,
        'sneeuw_mm': snow,
        'zonnestand': zonnestand,
        'locatie_naam': data['name'],
    }
