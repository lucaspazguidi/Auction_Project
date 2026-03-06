from flask import render_template, Blueprint, session, get_flashed_messages
from models.user import User
from models.bid import Bid
from models.item import Item
from models.auction import Auction
from models.transaction import Transaction
from sqlalchemy import desc

perfil_bp = Blueprint("perfil", __name__)
perfil_info_bp = Blueprint("perfil_info", __name__)

@perfil_bp.route("/perfil")
def perfil():
    # Get the specific user in DB
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)

    balance = user.balance if user.balance is not None else 0
    name = user.name
    email = user.email

    # Get all the user's active bids
    active_bids = Bid.query.join(Bid.auction).filter(
        Bid.user_id == user_id,
        Auction.situation == "active").count()    # .count return the number of registers
    
    my_bids = Bid.query.join(Bid.auction).filter(
        Bid.user_id == user_id,
        Auction.situation == "active").all()  
    
    bids = {}

    # Get the bid's situation
    for b in my_bids:
        leader_bid = Bid.query.filter_by(auction_id = b.auction_id).order_by(desc(Bid.bid_date)).limit(1).first()
        if leader_bid.bid_id == b.bid_id:
            situation = "Líder"
        else:
            situation = "Superado"

        bids[f"{b.bid_id}"] = (b, situation)

    # Return the amount of items that user has registered
    itens = Item.query.filter_by(user_id = user_id).count()

    # Get all the user transactions 
    transactions = Transaction.query.filter_by(user_id = user_id).order_by(desc(Transaction.transaction_date)).all()

    # Get the messages passed by flash, in other routes
    messages = get_flashed_messages()

    return render_template("dashboard.html", active_bids=active_bids, itens=itens, 
                           balance=balance, messages=messages, bids=bids, transactions=transactions,
                           name=name, email=email)

@perfil_info_bp.route("/perfil_info")
def perfil_info():
    # Get the specific user in DB
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)

    balance = user.balance if user.balance is not None else 0
    name = user.name
    email = user.email
    cel = user.cel
    cpf = user.cpf

    # Get all the user's active bids
    active_bids = Bid.query.join(Bid.auction).filter(
        Bid.user_id == user_id,
        Auction.situation == "active").count()

    # Return the amount of items that user has registered
    itens = Item.query.filter_by(user_id = user_id).count()

    messages = get_flashed_messages()

    return render_template("personal.html",balance=balance, name=name, email=email, cel=cel, cpf=cpf,
                           active_bids=active_bids, itens=itens, messages=messages)



    