from .db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

class Auction(db.Model):
    __tablename__ = "auction"

    auction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    start_date = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    min_bid = db.Column(db.Numeric(10, 2))
    starting_price = db.Column(db.Numeric(10, 2), nullable=False)
    situation = db.Column(Enum("active", "canceled", "finished", "arremat", "scheduled"), nullable=False)
    buy_now = db.Column(db.Numeric(10, 2))

    user = relationship("User")
    item = relationship("Item")

