from flask import session, redirect, request, url_for, render_template, Blueprint, make_response
from models.db import db
from sqlalchemy import or_
from utils.hash import verify_password
from models.user import User

login_bp = Blueprint("login", __name__)

@login_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user-email")
        password = request.form.get("password")

        # make a consult in db, get first user where name and email == user's input from the Form
        user = User.query.filter(or_(User.name == user, User.email == user)).first()

        if user:
            # Verify if the user's password saved in DB == to the input's password 
            if verify_password(password, user.password) == True:
                # Assign session variables
                session["logged"] = True
                session["name"] = user.name
                session["user_id"] = user.user_id
                
                # Setting cookie to save login
                resp = make_response(redirect(url_for("home.home")))
                resp.set_cookie("user_id", str(user.user_id), max_age=60*60)

                return resp


            else:
                message = "Usuário ou senha inválidos!"
                return render_template("login.html", message=message)
        
        else:
                message = "Usuário ou senha inválidos!"
                return render_template("login.html", message=message)

    return render_template("login.html")

