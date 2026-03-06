from flask import render_template, Blueprint
from models.auction import Auction
from models.bid import Bid
from models.category import Category
from datetime import datetime
from sqlalchemy import between, desc
from scheduler.scheduler import scheduler

home_bp = Blueprint("home", __name__)

@home_bp.route('/')
def home():
    # Active bids
    active_auctions = Auction.query.filter(Auction.situation == "active").count()

    # Highlights auctions
    highlights = Auction.query.filter(Auction.situation == "active").limit(16).all()

    # Today's bids number
    now = datetime.now()
    day = now.replace(microsecond=0, second=0, minute=0, hour=0)   # we only want to compare days
    max_day = now.replace(hour=23, minute=59, second=59, microsecond=99)
    print(day, max_day)

    # Use Between to get all the ocuurances in the respective interval and count to return a number 
    bids_today = Bid.query.filter(between(Bid.bid_date, day, max_day)).count()

    # auctions created today
    # Use Between to get all the ocuurances in the respective interval and count to return a number 
    auctions_today = Auction.query.filter(between(Auction.start_date, day, max_day)).count()

    # highest bid today
    # Use Between to get all the ocuurances in the respective interval and order by DESC to get the highest bid
    top_bid = Bid.query.filter(between(Bid.bid_date, day, max_day)).order_by(desc(Bid.value)).limit(1).first()
    
    if top_bid:
        value = top_bid.value
    else:
        value = 0

    # Get all the categories
    categories = Category.query.all()
    
    print(scheduler.get_jobs())
    for j in scheduler.get_jobs():
        print(j, j.id)


    return render_template('home.html', active_auctions=active_auctions, highlights=highlights,
                            bids_today=bids_today, auctions_today=auctions_today, value=value, categories=categories)