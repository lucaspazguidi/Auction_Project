from flask import Blueprint, session, redirect, url_for, request, flash
from models.user import User
from models.bid import Bid
from models.db import db
from models.auction import Auction
from sqlalchemy import desc, text
from datetime import datetime, timedelta
from scheduler.jobs import schedule_close
from socketio_instance import socketio

bid_bp = Blueprint("bid", __name__)

@bid_bp.route("/auction/<int:auction_id>/bid", methods=["POST"])
def bid(auction_id):

    value = request.form.get("value", type=float)

    # Valid field
    if not value:
        flash("Não é possível dar um lance sem valor!")
        return redirect(url_for("auction.auction", id=auction_id))

    user_id = session.get("user_id")

    if not user_id:
        flash("Você precisa estar logado.")
        return redirect(url_for("login.login"))

    try:

        # TRANSACTION START
        with db.session.begin():

            # LOCK no leilão
            db.session.execute(
                text("SELECT auction_id FROM auction WHERE auction_id = :id FOR UPDATE"),
                {"id": auction_id}
            )

            # Buscar leilão dentro da transação
            auction = Auction.query.get(auction_id)

            if not auction:
                flash("Leilão não encontrado.")
                return redirect(url_for("home.home"))

            if auction.situation != "active":
                flash("Este leilão não está ativo.")
                return redirect(url_for("auction.auction", id=auction_id))

            user = User.query.get(user_id)

            min_bid = float(auction.min_bid)

            if user_id == auction.user_id:
                flash("Você não pode dar lance no seu próprio leilão!")
                return redirect(url_for("auction.auction", id=auction_id))

            if not user.balance:
                flash("Saldo Insuficiente! Você tem R$0,00")
                return redirect(url_for("auction.auction", id=auction_id))

            # Maior lance atual
            highest_bid = Bid.query.filter_by(
                auction_id=auction_id
            ).order_by(desc(Bid.value)).first()

            if highest_bid:

                cur_bid = highest_bid.value

                if highest_bid.user_id == user_id:
                    flash("Você já é o lance líder!")
                    return redirect(url_for("auction.auction", id=auction_id))

            else:
                cur_bid = 0

            # Validação do valor do lance
            if value <= cur_bid:
                flash("O lance deve ser maior do que o atual")
                return redirect(url_for("auction.auction", id=auction_id))

            # incremento mínimo
            if min_bid != 0:
                if (value - float(cur_bid)) % min_bid != 0:
                    flash(f"O incremento mínimo é de R${min_bid}")
                    return redirect(url_for("auction.auction", id=auction_id))

            # saldo insuficiente
            if user.balance < value:
                flash(f"Saldo Insuficiente! Você tem R${user.balance}")
                return redirect(url_for("auction.auction", id=auction_id))

            # devolver saldo para o usuário que perdeu o lance
            if highest_bid:
                old_user = User.query.get(highest_bid.user_id)
                old_user.balance = float(old_user.balance) + float(highest_bid.value)

            # descontar saldo do novo lance
            user.balance = float(user.balance) - value

            # criar novo lance
            new_bid = Bid(
                user_id=user_id,
                auction_id=auction_id,
                value=value
            )

            db.session.add(new_bid)

        # TRANSACTION END (commit automático)

        # Extensão anti-sniper
        if auction.end_date - datetime.now() <= timedelta(minutes=1):

            auction.end_date = auction.end_date + timedelta(minutes=1)

            db.session.commit()

            schedule_close(auction)

        # 🔵 EMITIR EVENTO WEBSOCKET
        socketio.emit(
            "new_bid",
            {
                "auction_id": auction_id,
                "value": value,
                "end_date": auction.end_date.isoformat(),
                "user_id": user.name
            },
            room=f"auction_{auction_id}"
        )

        return redirect(url_for("auction.auction", id=auction_id))

    except Exception as e:

        db.session.rollback()

        print("Erro ao criar lance:", e)

        flash("Erro ao processar lance.")

        return redirect(url_for("auction.auction", id=auction_id))