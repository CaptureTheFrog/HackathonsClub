import json
import datetime

from models.hackathon import Hackathon

from flask_sqlalchemy import SQLAlchemy


def import_hackathons_to_db(db: SQLAlchemy):
    for h in json.loads(open('events.json', 'r').read()):
        hackathon = Hackathon(h['name'],
                              datetime.datetime.fromisoformat(h['start_date']),
                              datetime.datetime.fromisoformat(h['end_date']),
                              h['location_name'],
                              '',
                              'Hackathon',
                              '',
                              '',
                              '',
                              '',
                              None
                              )
        db.session.add(hackathon)
    db.session.commit()