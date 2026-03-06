from flask import Blueprint, session, request, redirect, url_for, flash
from models.user import User
from models.address import Adress
from models.db import db
from utils.validations.validate_cpf import validate_cpf

complete_register_bp = Blueprint("complete_register", __name__)

@complete_register_bp.route("/complete_register", methods=["POST"])
def complete_register():
    cpf_form = request.form.get("cpf")
    cep_form = request.form.get("cep")
    street = request.form.get("street")
    number = request.form.get("number")
    neighborhood = request.form.get("neighborhood")
    city = request.form.get("city")
    state = request.form.get("state")
    complement = request.form.get("complement")
    type = request.form.get("type")
    
    # transform cpf like 123.456.789-12 into 12345678912
    cpf = ""
    for c in cpf_form:
        if c.isdigit():
            cpf += c

    if not validate_cpf(cpf):
        flash("")
        flash("Insira um CPF válido!")
        return redirect(url_for('perfil_info.perfil_info'))
    
    # transform cep like 01223-012 into 01223012
    cep = ""
    for n in cep_form:
        if n.isdigit():
            cep += n

    user_id = int(session.get("user_id"))

    # return the user logged and make an update
    user = User.query.get(user_id)
    user.cpf = cpf

    # Creates new address instance
    address = Adress(
        user_id = user_id,
        street = street,
        neighborhood = neighborhood,
        city = city,
        state = state,
        number = number,
        cep = cep,
        type = type,
        complement = complement
    )

    db.session.add(address)
    db.session.commit()

    return redirect(url_for("perfil_info.perfil_info"))

