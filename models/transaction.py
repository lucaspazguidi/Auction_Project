from .db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

class Transaction(db.Model):
    __tablename__ = "transaction"

    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    type = db.Column(Enum('recharge', 'payment', 'receipt'), nullable=False)
    description = db.Column(db.String(255))
    value = db.Column(db.Numeric(10, 2))
    transaction_date = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)

    user = relationship("User")