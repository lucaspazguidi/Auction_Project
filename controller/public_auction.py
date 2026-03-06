from flask import render_template, redirect, url_for, session, Blueprint, request
from models.auction import Auction
from models.db import db
from datetime import datetime
from scheduler.jobs import schedule_close, schedule_open

public_auction_bp = Blueprint("public_auction", __name__)

@public_auction_bp.route("/public_auction", methods=["GET", "POST"])
def public_auction():
    if request.method == "POST":
        item = int(request.form.get("item"))   # Get item's id 
        price = float(request.form.get("price"))
        buy_now = float(request.form.get("buy_now"))
        min_bid = float(request.form.get("min_bid"))
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        now = datetime.now()     # Get current server's datetime
        date_now = now.replace(second=0, microsecond=0)   # Save only year/month/day/hour/min

        st_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")  # Convert string into date obj

        if st_date > date_now:
            situation = "scheduled"
        else:
            situation = "active"

        # Creating new Auction instance
        new_auction = Auction(
            user_id = session.get("user_id"),
            item_id = item,
            start_date = st_date,
            end_date = end_date,
            min_bid = min_bid,
            starting_price = price,
            situation = situation,
            buy_now = buy_now
        )

        # add new instance and save in DB
        db.session.add(new_auction)
        db.session.commit()

        if new_auction.situation == "scheduled":
            # Call the function to schedule the auction opening and closing
            schedule_open(new_auction)
            schedule_close(new_auction)
        else:
            # Call the function to schedule the auction closing
            schedule_close(new_auction)

        return redirect(url_for("home.home"))

    return render_template("sell.html")
