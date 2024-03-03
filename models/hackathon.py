from app import db, app
from user import User

class Hackathon(db.Model):
    __tablename__ = 'hackathon'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    instituion = db.Column(db.String(100))
    location = db.Column(db.String(100))
    event_type = db.Column(db.String(100))
    description = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    postal_address = db.Column(db.String(100))
    organisers = db.Column(db.ARRAY(db.Integer), db.ForeignKey(User.id))

    def __init__(self, title, date, institution, location, event_type, description, email, phone, postal_address, organisers):
        self.title = title
        self.date = date
        self.instituion = institution
        self.location = location
        self.event_type = event_type
        self.description = description
        self.email = email
        self.phone = phone
        self.postal_address = postal_address
        self.organisers = organisers