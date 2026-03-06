from flask import render_template, redirect, url_for, request, Blueprint, session
from models.item import Item
from models.db import db
from werkzeug.utils import secure_filename
import os 

register_item_bp = Blueprint("register_item", __name__)

@register_item_bp.route("/register_item", methods=["GET", "POST"])
def register_item():
    if request.method == "POST":
        name = request.form.get("name")
        category= int(request.form.get("category"))  # GET the category id
        description = request.form.get("description")

        image = request.files['image_file']   # Get the file's input
        filename = secure_filename(image.filename)
        path = os.path.join('static', 'images', filename)   # Return a string, that is the file's path
        image.save(path)   # Save the file in the respective path
        
        # Creating a new instance
        new_item = Item(
            name=name,
            description=description,
            user_id= session.get("user_id"),
            category_id = category,
            url_image = path    
        )

        # add new instance in session and saving in db
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for("home.home"))
    
    return render_template("item.html")
        