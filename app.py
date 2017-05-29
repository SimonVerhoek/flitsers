import json
from datetime import datetime

from flask import render_template
from sqlalchemy import or_, func

from model import app, MeldingSchema, Melding
from consts import TIME_SLOTS, RADAR, LASER, ANPR, CONTROLE_TYPES


meldingen_schema = MeldingSchema(many=True)

@app.route('/')
def home():
    q = Melding.query
    flitsers_today = q.filter_by(datum=datetime.now().date()).all()
    flitsers_total_count = q.count()
    first_flitser = q.first()

    # [0] for sending without metadata like 'errors'
    return render_template(
        'content.html',
        flitsers_today=meldingen_schema.dump(flitsers_today)[0],
        flitsers_total_count=flitsers_total_count,
        first_flitser_date=first_flitser.datum
    )


@app.route('/get_flitser_data')
def get_all_flitsers():
    q = Melding.query.all()

    flitsers = []
    for flitser in q:
        laatste_activiteit = None
        if flitser.laatste_activiteit:
            laatste_activiteit = flitser.laatste_activiteit.isoformat()

        flitsers.append({
            'id': flitser.id,
            'datum':flitser.datum.isoformat(),
            'soort_weg': flitser.soort_weg,
            'wegnummer': flitser.wegnummer,
            'zijde': flitser.zijde,
            'hm_paal': flitser.hm_paal,
            'type_controle': flitser.type_controle,
            'tijd_van_melden': flitser.tijd_van_melden.isoformat(),
            'details': flitser.details,
            'laatste_activiteit': laatste_activiteit,
            'locatie_lat': flitser.locatie_lat,
            'locatie_lon': flitser.locatie_lon,
            'weer_type': flitser.weer_type,
            'weer_beschrijving': flitser.weer_beschrijving,
            'weer_temp': flitser.weer_temp,
            'weer_temp_max': flitser.weer_temp_max,
            'weer_temp_min': flitser.weer_temp_min,
            'weer_luchtdruk_hpa': flitser.weer_luchtdruk_hpa,
            'weer_luchtvochtigheid_procent': flitser.weer_luchtvochtigheid_procent,
            'weer_windsnelheid_m_per_sec': flitser.weer_windsnelheid_m_per_sec,
            'weer_windrichting_graden': flitser.weer_windrichting_graden,
            'weer_bewolking_procent': flitser.weer_bewolking_procent,
            'weer_regen_mm': flitser.weer_regen_mm,
            'weer_sneeuw_mm': flitser.weer_sneeuw_mm,
            'weer_zonnestand': flitser.weer_zonnestand,
            'weer_locatie_naam': flitser.weer_locatie_naam,
        })

    return json.dumps({
        'flitsers': flitsers,
    })


@app.route('/get_chart_data')
def get_chart_data():
    base_q = Melding.query

    from time import time
    start = time()

    flitser_count_per_time_slot = {
        RADAR: [],  
        LASER: [],
        ANPR: [],
    }

    for ts in TIME_SLOTS:
        q = base_q.filter(or_(
            Melding.tijd_van_melden.between(ts.start, ts.stop),
            Melding.laatste_activiteit.between(ts.start, ts.stop)
        ))

        for type_controle in CONTROLE_TYPES:
            count = q.filter_by(type_controle=type_controle).count()
            flitser_count_per_time_slot[type_controle].append(int(count))
        


    from pprint import pprint
    pprint(flitser_count_per_time_slot)

    time_slots = [t.title for t in TIME_SLOTS]


    return json.dumps({
        'time_slots': time_slots,
        'flitser_count_per_time_slot': flitser_count_per_time_slot,
    })


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
