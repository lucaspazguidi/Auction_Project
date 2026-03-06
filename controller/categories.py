from flask import render_template, Blueprint
from models.category import Category

categories_bp = Blueprint("categories", __name__)

@categories_bp.route("/categories")
def categories():
    list_categories = Category.query.all()   # Get all categories registers in DB

    return render_template("categories.html",category=list_categories)
