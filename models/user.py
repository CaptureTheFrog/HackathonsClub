import bcrypt
from flask_login import UserMixin
from db import db

# TODO edit functionality
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')

    def __init__(self, email, password, role):
        self.email = email
        self.password = self.encrypt_password(password)
        self.role = role

    # password hashing
    @staticmethod
    def encrypt_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # password verification
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
