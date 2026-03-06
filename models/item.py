from .db import db
from sqlalchemy.orm import relationship

class Item(db.Model):
    __tablename__ = "item"

    item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    url_image = db.Column(db.String(255), nullable=False)
   
    user = relationship("User")
    category = relationship("Category")