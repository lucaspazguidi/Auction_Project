from flask import render_template, redirect, url_for, session, Blueprint, request
from models.auction import Auction
from models.db import db
from datetime import datetime
from scheduler.jobs import close_auction, public_auction as open_auction

public_auction_bp = Blueprint("public_auction", __name__)


@public_auction_bp.route("/public_auction", methods=["GET", "POST"])
def create_public_auction():

    if request.method == "POST":

        item = int(request.form.get("item"))
        price = float(request.form.get("price"))
        buy_now = float(request.form.get("buy_now"))
        min_bid = float(request.form.get("min_bid"))

        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        # Convertendo datas
        st_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        en_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")

        now = datetime.now().replace(second=0, microsecond=0)

        # Definir situação inicial
        if st_date > now:
            situation = "scheduled"
        else:
            situation = "active"

        # Criar leilão
        new_auction = Auction(
            user_id=session.get("user_id"),
            item_id=item,
            start_date=st_date,
            end_date=en_date,
            min_bid=min_bid,
            starting_price=price,
            situation=situation,
            buy_now=buy_now
        )

        db.session.add(new_auction)
        db.session.commit()

        # Se o leilão começa no futuro
        if new_auction.situation == "scheduled":

            # Agenda abertura
            open_auction(new_auction.auction_id)

            # Agenda fechamento
            close_auction(new_auction.auction_id)

        else:
            # Apenas agenda fechamento
            close_auction(new_auction.auction_id)

        return redirect(url_for("home.home"))

    return render_template("sell.html")