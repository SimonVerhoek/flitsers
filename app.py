from datetime import datetime

from flask import render_template

from model import app, MeldingSchema, Melding


meldingen_schema = MeldingSchema(many=True)

@app.route('/')
def home():
  q = Melding.query
  flitsers_today = q.filter_by(datum=datetime.now().date()).all()
  all_flitsers = q.all()

  # [0] for sending without metadata like 'errors'
  return render_template(
    'content.html',
    flitsers=meldingen_schema.dump(all_flitsers)[0],
    flitsers_today=meldingen_schema.dump(flitsers_today)[0]
  )


if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
