from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    nome = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    senha = db.Column(db.String(150))
    