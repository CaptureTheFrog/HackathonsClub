from app import db, app
from user import User

class Sponsor(db.Model):
    __tablename__ = 'sponsor'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100)) 
    company_logo = db.Column(db.BLOB) 
    company_email = db.Column(db.String(100)) 
    company_phone = db.Column(db.String(100))
    company_website = db.Column(db.String(100)) 
