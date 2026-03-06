from models.auction import Auction
from models.bid import Bid
from models.user import User
from models.transaction import Transaction
from models.db import db
from sqlalchemy import desc
from .scheduler import scheduler
from decimal import Decimal

# Function that will be used as param in the main function to schedule jobs
def close_auction(auction_id):
    # late import
    from app import app
    # Open context
    with app.app_context():
        # The auction to be closed
        auction = Auction.query.get(int(auction_id))

        # Validations
        if not auction:
            return   # interrupt the actual job
        
        if auction.situation != "active":
            return   # interrupt the actual job

        # update the auction's situation, close auction
        # close here to avoid incomplete bids
        auction.situation = "finished"
        
        # Find the winner bid, do transaction
        winner_bid = Bid.query.filter_by(auction_id = auction_id).order_by(desc(Bid.bid_date)).limit(1).first()

        if winner_bid:
            # winner user makes transaction for auction's owner
            payment_transaction = Transaction(
                user_id = winner_bid.user_id,   # user that did winner_bid
                type = "payment",
                description = f"Lance vencedor. Efetuando pagamento para dono do leilão",
                value = float(winner_bid.value)
            )

            # Auction's owner receipt the payment
            receipt_transaction = Transaction(
                user_id = auction.user_id,   # Auction's owner
                type = "receipt",
                description = f"Leilão finalizado. Recebendo o valor/pagamento do lance vencedor",
                value = float(winner_bid.value)
            )

            # update auction owner's balance
            auction_owner = User.query.get(auction.user_id)
            auction_owner.balance = Decimal(auction_owner.balance) + Decimal(winner_bid.value)

            # Add the new registers
            db.session.add(payment_transaction)
            db.session.add(receipt_transaction)

            # Save the updates and new registers in DB
            db.session.commit()

        else:
            db.session.commit()
            return  # interrupt the actual job

def schedule_close(auction):

    # schedule job
    scheduler.add_job(
        func=close_auction,    # function that will be executed
        trigger="date",
        run_date = auction.end_date,    # job's date execution
        args=[auction.auction_id],      # args that function will receive
        id=f"close_{auction.auction_id}",     # Job's ID
        replace_existing=True,    # If a job with the same id exist, then replace
        coalesce=True,              # avoid execut repetitions
        misfire_grace_time=30      # accept lates executions
    )

def public_auction(auction_id):

    # late import
    from app import app
    
    with app.app_context():

        auction = Auction.query.get(int(auction_id))

        # Validations
        if not auction:
            return
        
        if auction.situation != "scheduled":
            return

        # Change the situation to Active and then the routes will start to show this auction as active 
        auction.situation = "active"

        # Save the updates
        db.session.commit()
        return

def schedule_open(auction):
    # schedule job
    scheduler.add_job(
        func=public_auction,
        trigger='date',
        run_date=auction.start_date,
        args=[auction.auction_id],
        id=f"open_{auction.auction_id}",
        replace_existing=True,
        coalesce=True,
        misfire_grace_time=30
    )
