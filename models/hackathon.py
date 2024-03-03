from db import db


class Hackathon(db.Model):
    __tablename__ = 'hackathon'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100))
    postal_address = db.Column(db.String(100))

    def __init__(self, title, start_date, end_date, institution, location, event_type, description, email, phone, postal_address, organisers):
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.institution = institution
        self.location = location
        self.event_type = event_type
        self.description = description
        self.email = email
        self.phone = phone
        self.postal_address = postal_address
        #self.organisers = organisers