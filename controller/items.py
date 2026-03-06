from flask import Blueprint, render_template, session, request
from models.item import Item
from models.auction import Auction
from models.db import db


items_bp = Blueprint("items", __name__)
item_info_bp = Blueprint('item_info', __name__)

@items_bp.route("/items")
def items():
    user_id = int(session.get('user_id'))
    situation = request.args.get('situation')

    # Get all the items created by user X
    query = Item.query
    filters = [Item.user_id == user_id]   # default filter

    if situation == "auction":
        query = query.join(Auction.item)
        filters.pop(0)
        filters.append(Auction.user_id == user_id)
    
    if situation == "all":
        query.join(Auction.item)
        filters.append(Auction.user_id == user_id)
    
    if situation == "draft":
        sub = db.session.query(Auction.item_id).filter(Auction.user_id == user_id)   # sub query
        filters.append(~Item.item_id.in_(sub))  # ~ means not
        
    my_items = query.filter(*filters).all()

    return render_template("items.html", my_items=my_items)


@item_info_bp.route("/item_info/<int:id>")
def item_info(id):
    item = Item.query.get(id)
    auctions = Auction.query.filter_by(item_id = id).all()  # Get all the auctions with this item
    
    return render_template("item-details.html", item=item, auctions=auctions)
