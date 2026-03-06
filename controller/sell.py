from flask import render_template, Blueprint, session, jsonify
from models.item import Item

sell_bp = Blueprint("sell", __name__)
api_item_bp = Blueprint("api_item", __name__)

@sell_bp.route("/sell")
def sell():
    # Get all the resgistered items from user X
    items = Item.query.filter_by(user_id = session.get("user_id")).all()

    return render_template("sell.html", items=items)

@api_item_bp.route("/api/item/<int:id>")
def item_info(id):
    item = Item.query.filter_by(item_id = id).one()

    return jsonify({
        "desc": item.description,
        "image": item.url_image
    })
