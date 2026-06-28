import logging
import os
import time
from datetime import datetime

import db
import requests
from consts import ANWB_API_URL
from model import Melding
from scrapefunctions import get_weather
from sqlalchemy.orm import Session

TOR_PROXIES = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050",
}


def get_flitsers():
    today = datetime.today().strftime("%Y-%m-%d")
    r = requests.get(ANWB_API_URL, proxies=TOR_PROXIES)
    if r.status_code != 200:
        msg = f"ANWB API request failed: HTTP {r.status_code}"
        logging.error(msg)
        raise ValueError(msg)
    process_flitsers(data=r.json(), today=today)


def process_flitsers(data, today):
    new_count = 0
    updated_count = 0

    with Session(db.engine) as ses:
        for road in data["roads"]:
            for segment in road["segments"]:
                for radar in segment.get("radars", []):
                    wegnummer = radar["road"]
                    soort_weg = "snelweg" if radar["type"] == "a" else "nweg"
                    rijrichting = radar["from"] + " richting " + radar["to"]
                    hm_paal = str(radar["HM"])
                    details = radar["reason"]

                    seen = (
                        ses.query(Melding)
                        .filter_by(datum=today, wegnummer=wegnummer, details=details)
                        .first()
                    )

                    if seen:
                        seen.laatste_activiteit = datetime.now().time()
                        updated_count += 1
                    else:
                        m = Melding()
                        m.soort_weg = soort_weg
                        m.wegnummer = wegnummer
                        m.rijrichting = rijrichting
                        m.hm_paal = hm_paal
                        m.details = details
                        m.tijd_van_melden = datetime.now().time()

                        if "loc" in radar:
                            lat = radar["loc"]["lat"]
                            lon = radar["loc"]["lon"]
                            m.locatie_lat = lat
                            m.locatie_lon = lon
                            m.locatie = f"{lat},{lon}"

                            weather = get_weather(lat=lat, lon=lon, time_unix=int(time.time()))
                            m.weer_type = weather["type"]
                            m.weer_beschrijving = weather["beschrijving"]
                            m.weer_temp = weather["temp"]
                            m.weer_temp_max = weather["temp_max"]
                            m.weer_temp_min = weather["temp_min"]
                            m.weer_luchtdruk_hpa = weather["luchtdruk_hpa"]
                            m.weer_luchtvochtigheid_procent = weather["luchtvochtigheid_procent"]
                            m.weer_windsnelheid_m_per_sec = weather["windsnelheid_m_per_sec"]
                            m.weer_windrichting_graden = weather["windrichting_graden"]
                            m.weer_bewolking_procent = weather["bewolking_procent"]
                            m.weer_regen_mm = weather["regen_mm"]
                            m.weer_sneeuw_mm = weather["sneeuw_mm"]
                            m.weer_zonnestand = weather["zonnestand"]
                            m.weer_locatie_naam = weather["locatie_naam"]

                        ses.add(m)
                        new_count += 1

                    ses.commit()

    print(f"Done: {new_count} new, {updated_count} updated.")


if __name__ == "__main__":
    get_flitsers()
