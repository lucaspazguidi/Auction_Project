from .db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

class Adress(db.Model):
    __tablename__ = "address"

    address_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    street = db.Column(db.String(100), nullable=False)
    neighborhood = db.Column(db.String(40), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    cep = db.Column(db.String(8))
    type = db.Column(Enum('house', 'apartment'), nullable=False)
    complement = db.Column(db.String(50))

    user = relationship("User")