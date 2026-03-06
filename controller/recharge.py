from flask import Blueprint, render_template, session, request, redirect, url_for
from models.user import User
from models.transaction import Transaction
from models.db import db

recharge_bp = Blueprint("recharge", __name__)

@recharge_bp.route("/recharge", methods=["POST"])
def recharge():
     # Get the user instance
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)

    if not user.cpf:
        message = "Você precisa concluir cadastro para efetuar uma recarga"
        return render_template("balance.html", message=message)

    if request.method == "POST":
        value = request.form.get("recharge_amount", type=float)
        custom = request.form.get("custom_amount", type=float)

        print(request.form)

        if custom:
            amount = custom
        else:
            amount = value

        if amount < 10:
            message = "O Valor mínimo para recarga é de R$10,00"
            return render_template("balance.html", message=message)   

        # Do an update
        if user.balance == None:
            current_balance = 0
        else:
            current_balance = user.balance

        user.balance = float(current_balance) + amount

        transaction = Transaction(
            user_id = user_id,
            type = "recharge",
            description = "Recarga de saldo",
            value = amount   
        )

        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for("perfil.perfil"))

    return render_template("balance.html")



