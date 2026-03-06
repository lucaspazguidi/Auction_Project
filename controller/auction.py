from flask import Blueprint, render_template, get_flashed_messages, abort
from models.auction import Auction
from models.bid import Bid
from sqlalchemy import desc
from sqlalchemy.exc import NoResultFound

auction_bp = Blueprint("auction", __name__)

@auction_bp.route("/auction/<int:id>")
def auction(id):
    # get the auction with the id passed by url
    try:
        auction = Auction.query.filter_by(auction_id = id).one()
    except NoResultFound:
        abort(404)

    # Get the image's url 
    image = auction.item.url_image

    # get all the bids in the respective auction
    bids = Bid.query.filter_by(auction_id = id).all()

    # get the current bid
    bid = Bid.query.filter_by(auction_id = id).order_by(desc(Bid.bid_date)).limit(1).first()
    
    if bid:
        current_bid = bid.value
    else:
        current_bid = 0

    messages = get_flashed_messages()

    return render_template("auction.html", auction=auction, bids=bids, current_bid=current_bid, messages=messages, image=image)

