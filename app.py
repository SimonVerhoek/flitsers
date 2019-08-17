import os
from datetime import datetime
from typing import List

from flask import render_template, request, jsonify
from sqlalchemy import or_
from sqlalchemy.orm.query import Query

from model import app, Melding
from consts import TIME_SLOTS, CONTROLE_TYPES


@app.route('/')
def home():
    q = Melding.query

    flitsers_total_count = q.count()
    first_flitser = q.order_by(Melding.datum).first()

    q_today = q.filter_by(datum=datetime.now().date())
    flitsers_today = q_today.all()

    datasets = get_datasets(query=q_today)

    time_slots = [
        (t.title, f'({t.start.strftime("%H:%M")}-{t.stop.strftime("%H:%M")}u)')
        for t in TIME_SLOTS
    ]

    return render_template(
        'content.html',
        flitsers_today=[flitser._asdict() for flitser in flitsers_today],
        flitsers_total_count=flitsers_total_count,
        first_flitser_date=first_flitser.datum,
        datasets=datasets,
        time_slots=time_slots,
        last_updated=dir_last_updated('static/js')
    )


@app.route('/get_chart_data', methods=['POST'])
def get_chart_data():
    base_q = Melding.query

    # if start and stop given as input from frontend, only query those
    args = request.json
    if args:
        moment_start = args['start']
        moment_stop = args['stop']

        base_q = base_q.filter(Melding.datum.between(moment_start, moment_stop))

    datasets = get_datasets(query=base_q)

    flitsers = [flitser._asdict() for flitser in base_q.all()]

    return jsonify({
        'datasets': datasets,
        'speeding_cams': flitsers
    })


def get_datasets(query: Query) -> List[dict]:
    """
    Prepares datasets for bar chart.

    :param query:   a Query object for Melding objects
    :return:        Melding object data per type_controle
    """
    datasets = []

    for type_controle in CONTROLE_TYPES:
        dataset = {
            'label': type_controle,
            'data': []
        }
        if type_controle == 'Radar':
            dataset['backgroundColor'] = 'rgb(63, 127, 191)'
        elif type_controle == 'Laser':
            dataset['backgroundColor'] = 'rgba(63, 127, 191, 0.6)'
        else:
            dataset['backgroundColor'] = 'rgba(63, 127, 191, 0.2)'

        q = query.filter_by(type_controle=type_controle)

        for ts in TIME_SLOTS:
            count = q.filter(or_(
                Melding.tijd_van_melden.between(ts.start, ts.stop),
                Melding.laatste_activiteit.between(ts.start, ts.stop)
            )).count()
            dataset['data'].append(int(count))

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
    return str(max(os.path.getmtime(os.path.join(root_path, f))
               for root_path, dirs, files in os.walk(folder)
               for f in files))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
