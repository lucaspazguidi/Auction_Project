from flask import request, Blueprint, render_template, jsonify, session
from models.db import db
from utils.hash import hash_password
from sqlalchemy import text
from utils.validations.validate_username import validate_username
from utils.validations.valid_email import valid_email

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    # GET → first access, just render template
    if request.method == "GET":
        return render_template("register.html")

    # POST → fetch → JSON
    data = request.get_json()

    # form fields
    name = data.get("name")
    email = data.get("email")
    cel = data.get("cel")
    password = data.get("password")
    confirm = data.get("confirm")

    
    # The fields must be equal
    if password != confirm:
        return jsonify({
            "error": True,
            "field": "confirm",
            "message": "As senhas não coincidem!"
        }), 400

    # User's name validation
    if not validate_username(name):
        return jsonify({
            "error": True,
            "field": "name",
            "message": "Já existe um usuário com esse nome!"
        }), 400

    # Email's Validation
    if not valid_email(email):
        return jsonify({
            "error": True,
            "field": "email",
            "message": "Insira um email válido!"
        }), 400

    # Tranform de password into a hash
    h_password = hash_password(password)

    try:
        # Calling db procedure that create a new user
        result = db.session.execute(
            text("CALL register_user(:name, :email, :password, :cel)"),
            {"name": name, "email": email, "password": h_password, "cel": cel}
        )

        db.session.commit()

    # Except some error
    except Exception as e:
        print("Erro no banco →", e)
        return jsonify({
            "error": True,
            "field": "name",
            "message": "Erro ao criar conta. Tente outro nome ou email."
        }), 500


    # The new user was created, now redirect for login route
    return jsonify({
        "success": True,
        "redirect": "/login" 
    })


