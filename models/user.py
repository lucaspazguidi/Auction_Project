from .db import db

class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Numeric(10, 2))
    cel = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(255))
    adm = db.Column(db.Boolean)
 