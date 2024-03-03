from app import db, app


class Sponsor(db.Model):
    __tablename__ = 'sponsor'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100)) 
    company_logo = db.Column(db.String(100)) 
    company_email = db.Column(db.String(100)) 
    company_phone = db.Column(db.String(100))
    company_website = db.Column(db.String(100)) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    user = db.relationship('User', backref='sponsor', uselist=False, primaryjoin="Sponsor.user_id == User.id")

    def __init__(self, name, logo, email, phone, website, login):
        self.company_name = name
        self.company_logo = logo
        self.company_email = email
        self.company_phone = phone
        self.company_website = website
        self.user_id = login