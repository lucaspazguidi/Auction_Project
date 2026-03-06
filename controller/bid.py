from flask import Blueprint, session, redirect, url_for, request, flash
from models.user import User
from models.bid import Bid
from models.db import db
from models.auction import Auction
from sqlalchemy import desc
from datetime import datetime, timedelta
from scheduler.jobs import schedule_close

bid_bp = Blueprint("bid", __name__)

@bid_bp.route("/auction/<int:auction_id>/bid", methods=["POST"])
def bid(auction_id):
    value = request.form.get("value", type=float)
    
    # Valid field, if value != Null
    if not value:
        flash("Não é possível dar um lance sem valor!")
        return redirect(url_for("auction.auction", id=auction_id))
    
    # Get the user logged
    user_id = int(session.get("user_id"))
    user = User.query.get(user_id)

    # Get the auction in DB
    auction = Auction.query.get(int(auction_id))
    min = float(auction.min_bid)

    if user_id == auction.user_id:
        flash("Você não pode dar lance no seu próprio leilão!")
        return redirect(url_for('auction.auction', id=auction_id))
    
     # The user doesn't have any balance
    if not user.balance:
        flash("Saldo Insuficiente! Você tem R$0,00")
        return redirect(url_for("auction.auction", id=auction_id))

    
    # Current bid
    bid = Bid.query.filter_by(auction_id = auction_id).order_by(desc(Bid.bid_date)).limit(1).first()

    # if a current bid exists
    if bid:
        cur_bid = bid.value
        # if the user that is winning wants to do another bid
        if bid.user_id == user_id:
            flash("Você já é o lance líder!")
            return redirect(url_for('auction.auction', id=auction_id))
    else:
        cur_bid = 0

    if cur_bid:
        if value <= cur_bid:
            flash("O lance deve ser maior do que o atual")
            return redirect(url_for("auction.auction", id=auction_id))
        
    
    # if the bid value don't follow the min_bid increment rule
    if min != 0:
        if (value - float(cur_bid)) % min != 0:
            flash(f"O incremento mínimo é de R${min}")
            return redirect(url_for("auction.auction", id=auction_id))
    
    # If the user doesn't have enough balance
    if user.balance < value:
        flash(f"Saldo Insuficiente! Você tem R${user.balance} e precisa de R${value - float(user.balance)}")
        return redirect(url_for("auction.auction", id=auction_id))
    
    if bid:
        # refund the last bid user's balance 
        # the bid var, became previous bid
        old_user = User.query.get(bid.user_id)
        old_user.balance = float(old_user.balance) + float(bid.value)

    # Everything ok, update the balance
    cur_balance = user.balance
    user.balance = float(cur_balance) - value

    # Create a new bid register
    new_bid = Bid(
        user_id = user_id,
        auction_id = int(auction_id),
        value = value
    )

    db.session.add(new_bid)

    # Save all the changes, including updates
    db.session.commit()


    # the difference between two datetime objs return another obj wich is datetime.timedelta()
    if auction.end_date - datetime.now() <= timedelta(minutes=1):
        # reset end_date to 1 min
        auction.end_date = auction.end_date + timedelta(minutes=1)
        db.session.commit()

        # reschedule the job
        schedule_close(auction)

    return redirect(url_for("auction.auction", id = auction_id))


    








