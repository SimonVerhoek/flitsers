import logging
from datetime import datetime

import requests
from consts import (
    NA_ZONSONDERGANG,
    NA_ZONSOPGANG,
    OPENWEATHER_API_URL,
    OPENWEATHER_APP_ID,
    VOOR_ZONSOPGANG,
)


def get_weather(lat, lon, time_unix):
    params = {
        "appid": OPENWEATHER_APP_ID,
        "units": "metric",
        "lang": "nl",
        "lat": lat,
        "lon": lon,
    }
    r = requests.get(OPENWEATHER_API_URL, params=params)
    if r.status_code != 200:
        raise ValueError(f"OpenWeather API error {r.status_code}: {r.text}")
    data = r.json()

    # Openweather API rain & snow key seems to vary between "1h" and "3h",
    # so if it exists just get the first value found and be done with it
    rain = list(data["rain"].values())[0] if "rain" in data else None
    snow = list(data["snow"].values())[0] if "snow" in data else None

    zonnestand = None
    sys_data = data.get("sys", {})
    if sys_data:
        if time_unix <= sys_data["sunrise"]:
            zonnestand = VOOR_ZONSOPGANG
        elif time_unix >= sys_data["sunset"]:
            zonnestand = NA_ZONSONDERGANG
        else:
            zonnestand = NA_ZONSOPGANG

    return {
        "type": data["weather"][0]["main"],
        "beschrijving": data["weather"][0]["description"],
        "temp": data["main"]["temp"],
        "temp_max": data["main"]["temp_max"],
        "temp_min": data["main"]["temp_min"],
        "luchtdruk_hpa": data["main"]["pressure"],
        "luchtvochtigheid_procent": data["main"]["humidity"],
        "windsnelheid_m_per_sec": data["wind"]["speed"],
        "windrichting_graden": data["wind"]["deg"],
        "bewolking_procent": data["clouds"]["all"],
        "regen_mm": rain,
        "sneeuw_mm": snow,
        "zonnestand": zonnestand,
        "locatie_naam": data["name"],
    }
