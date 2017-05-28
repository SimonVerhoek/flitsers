import csv

from sqlalchemy import *

from model import db, Melding


def export_to_csv():
    """
    Enables csv exports for analytical purposes.
    """
    meldingen = Melding.query.all()
   
    data = []

    for m in meldingen:
        data.append({
            'id': m.id,
            'datum': m.datum,
            'soort_weg': m.soort_weg,
            'wegnummer': m.wegnummer,
            'zijde': m.zijde,
            'hm_paal': m.hm_paal,
            'type_controle': m.type_controle,
            'tijd_van_melden': m.tijd_van_melden,
            'laatste_activiteit': m.laatste_activiteit,
        })
    
    keys = data[0].keys()
    with open('flitsers_export.csv', 'wb') as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
        

if __name__ == '__main__':
    export_to_csv()
