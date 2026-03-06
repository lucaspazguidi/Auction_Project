from .db import db
from sqlalchemy.orm import relationship

class Bid(db.Model):
    __tablename__ = "bid"

    bid_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey("auction.auction_id"), nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    bid_date = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    user = relationship("User")
    auction = relationship("Auction")