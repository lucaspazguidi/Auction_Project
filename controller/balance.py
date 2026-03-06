from flask import Blueprint, render_template, session
from models.user import User
from models.transaction import Transaction
from sqlalchemy import desc

balance_bp = Blueprint("balance", __name__)

@balance_bp.route("/balance")
def balance():
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)

    # Get the last recharge transaction
    last_transaction = Transaction.query.filter(Transaction.user_id == user_id, Transaction.type == "recharge").order_by(desc(Transaction.transaction_date)).limit(1).first()
    
    balance = user.balance
    cpf = user.cpf

    return render_template("balance.html", cpf=cpf, balance=balance, last_transaction=last_transaction)