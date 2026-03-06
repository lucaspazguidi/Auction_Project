from flask import Blueprint, redirect, url_for, session, request, render_template, flash
from models.user import User
from utils.validations.valid_email import valid_email
from utils.validations.validate_username import validate_username
from models.db import db
from utils.hash import verify_password, hash_password

update_basic_info_bp = Blueprint("update_basic_info", __name__)
update_password_bp = Blueprint('update_password', __name__)

@update_basic_info_bp.route("/update_basic_info", methods=["POST", "GET"])
def update_basic_info():
    name = request.form.get("name")
    email = request.form.get("email")
    cel = request.form.get("cel")

    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)

    if name:
        if validate_username(name):
            user.name = name
        else:
            flash("Já existe um usuário com esse nome!")
            return redirect(url_for('perfil_info.perfil_info'))
    
    if email:
        if valid_email(email):
            user.email = email
        else:
            flash("Insira um email válido")
            return redirect(url_for('perfil_info.perfil_info'))
    
    if cel:

        new_cel = ""
        for c in cel:
            if c.isdigit():
                new_cel += c
        
        if len(new_cel) != 11:
            flash("Insira um número de celular válido!")
            return redirect(url_for("perfil_info.perfil_info"))
        user.cel = new_cel

    
    db.session.commit()   # Commit the changes

    return redirect(url_for("perfil_info.perfil_info"))

@update_password_bp.route("/update_password", methods=["POST"])
def update_password():
    cur_password = request.form.get("current")
    new_password = request.form.get("new")
    confirm = request.form.get("confirm")

    if new_password != confirm:
        flash("")
        flash("")
        flash("As senhas não coincidem!")
        return redirect(url_for("perfil_info.perfil_info"))

    user_id = int(session.get('user_id'))
    user = User.query.get(user_id)

    # Verify if user knows the current password
    if verify_password(cur_password, user.password):
        new_p = hash_password(new_password)
        user.password = new_p

        # save the changes
        db.session.commit()
        return redirect(url_for('perfil_info.perfil_info'))
    
    flash("")
    flash("")
    flash("Senha Incorreta!")
    return redirect(url_for('perfil_info.perfil_info'))

        
