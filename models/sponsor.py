from app import db, app


class Sponsor(db.Model):
    __tablename__ = 'sponsor'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100)) 
    company_logo = db.Column(db.String(100)) 
    company_email = db.Column(db.String(100)) 
    company_phone = db.Column(db.String(100))
    company_website = db.Column(db.String(100)) 
    login_id = db.Column(db.Integer)

    def __init__(self, name, logo, email, phone, website, login):
        self.company_name = name
        self.company_logo = logo
        self.company_email = email
        self.company_phone = phone
        self.company_website = website
        self.login_id = login