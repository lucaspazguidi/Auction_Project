from flask import render_template, Blueprint
from models.category import Category

item_bp = Blueprint("item", __name__)

@item_bp.route("/item")

def item():
    categories = Category.query.all()

    return render_template("item.html", categories=categories)
