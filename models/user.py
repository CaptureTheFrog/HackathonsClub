from app import db, app

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(255))
    role = db.Column(db.String(100))

    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role
