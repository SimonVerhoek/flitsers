import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

import db
from consts import CONTROLE_TYPES, MAPBOX_ACCESS_TOKEN, TIME_SLOTS
from model import Melding
from schemas.melding import MeldingSchema


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    with Session(db.engine) as ses:
        q = ses.query(Melding)

        flitsers_total_count = q.count()
        first_flitser = q.order_by(Melding.datum).first()

        q_today = q.filter_by(datum=datetime.now().date())
        flitsers_today = q_today.all()

        datasets = get_datasets(query=q_today)

        time_slots = [
            (t.title, f'({t.start.strftime("%H:%M")}-{t.stop.strftime("%H:%M")}u)')
            for t in TIME_SLOTS
        ]

        return templates.TemplateResponse(
            name="content.html",
            context={
                "request": request,
                "context": dict(
                    flitsers_today=[MeldingSchema.model_validate(melding).model_dump() for melding in flitsers_today],
                    flitsers_total_count=flitsers_total_count,
                    first_flitser=MeldingSchema.model_validate(first_flitser).model_dump(),
                    datasets=datasets,
                    time_slots=time_slots,
                    last_updated=dir_last_updated("static/js"),
                    mapbox_acess_token=MAPBOX_ACCESS_TOKEN,
                ),
            }

        )


@app.get("/get_chart_data")
def get_chart_data(start: str, stop: str):
    with Session(db.engine) as ses:
        q = ses.query(Melding).filter(Melding.datum.between(start, stop))

        datasets = get_datasets(query=q)

        flitsers = [MeldingSchema.model_validate(melding).model_dump() for melding in q.all()]

        return {"datasets": datasets, "speeding_cams": flitsers}


def get_datasets(query: Query) -> List[dict]:
    """
    Prepares datasets for bar chart.

    :param query:   a Query object for Melding objects
    :return:        Melding object data per type_controle
    """
    datasets = []

    for type_controle in CONTROLE_TYPES:
        dataset = {"label": type_controle, "data": []}
        if type_controle == "Radar":
            dataset["backgroundColor"] = "rgb(63, 127, 191)"
        elif type_controle == "Laser":
            dataset["backgroundColor"] = "rgba(63, 127, 191, 0.6)"
        else:
            dataset["backgroundColor"] = "rgba(63, 127, 191, 0.2)"

        q = query.filter_by(type_controle=type_controle)

        for ts in TIME_SLOTS:
            count = q.filter(
                or_(
                    Melding.tijd_van_melden.between(ts.start, ts.stop),
                    Melding.laatste_activiteit.between(ts.start, ts.stop),
                )
            ).count()
            dataset["data"].append(int(count))

        datasets.append(dataset)

    return datasets


def dir_last_updated(folder: str) -> str:
    """
    Creates a string with the given folder's last update time.
    Is used for JS file versioning.
    Big thanks to: https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file#answer-54164514

    :param folder:  a static folder that should be versioned
    :return:        a new version number
    """
    return str(
        max(
            os.path.getmtime(os.path.join(root_path, f))
            for root_path, dirs, files in os.walk(folder)
            for f in files
        )
    )
