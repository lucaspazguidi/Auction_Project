from models.auction import Auction
from models.bid import Bid
from models.user import User
from models.transaction import Transaction
from models.db import db
from sqlalchemy import desc
from decimal import Decimal
from datetime import datetime

# Function responsible for closing auctions
def close_auction(auction_id):

    from app import app

    with app.app_context():

        auction = Auction.query.get(int(auction_id))

        # Validations
        if not auction:
            return

        if auction.situation != "active":
            return

        # Close auction
        auction.situation = "finished"

        # Find the highest bid (winner)
        winner_bid = Bid.query.filter_by(
            auction_id=auction_id
        ).order_by(desc(Bid.value)).first()

        if winner_bid:

            payment_transaction = Transaction(
                user_id=winner_bid.user_id,
                type="payment",
                description="Lance vencedor. Efetuando pagamento para dono do leilão",
                value=float(winner_bid.value)
            )

            receipt_transaction = Transaction(
                user_id=auction.user_id,
                type="receipt",
                description="Leilão finalizado. Recebendo o valor do lance vencedor",
                value=float(winner_bid.value)
            )

            # Update auction owner's balance
            auction_owner = User.query.get(auction.user_id)

            if auction_owner.balance is None:
                auction_owner.balance = Decimal(0)

            auction_owner.balance = Decimal(auction_owner.balance) + Decimal(winner_bid.value)

            db.session.add(payment_transaction)
            db.session.add(receipt_transaction)

        db.session.commit()


# Function that checks expired auctions
def check_expired_auctions():

    from app import app

    with app.app_context():

        now = datetime.utcnow()

        expired_auctions = Auction.query.filter(
            Auction.situation == "active",
            Auction.end_date < now
        ).all()

        for auction in expired_auctions:
            close_auction(auction.auction_id)


# Function responsible for opening auctions
def public_auction(auction_id):

    from app import app

    with app.app_context():

        auction = Auction.query.get(int(auction_id))

        if not auction:
            return

        if auction.situation != "scheduled":
            return

        auction.situation = "active"

        db.session.commit()


# Function that checks auctions that should start
def check_scheduled_auctions():

    from app import app

    with app.app_context():

        now = datetime.utcnow()

        auctions = Auction.query.filter(
            Auction.situation == "scheduled",
            Auction.start_date < now
        ).all()

        for auction in auctions:
            public_auction(auction.auction_id)