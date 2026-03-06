from flask import Blueprint, request, jsonify, render_template
from models.auction import Auction
from models.item import Item
from models.category import Category

api_auctions_bp = Blueprint("api_auctions", __name__)
auctions_bp = Blueprint("list_auctions", __name__)

@api_auctions_bp.route("/api/auctions")
def api_auctions():
    page = request.args.get("page", 1, type=int)
    per_page = 16
    category = request.args.get("category", type=int)  # Category id
    situation = request.args.get("situation")

    filters = [Auction.situation == "active"]    # will store the boolean expressions
    query = Auction.query

    categories = Category.query.all()

    # Show all auctions
    if situation == "all":
        # if the user selected some category
        if category:
            auctions = query.join(Auction.item).filter(Item.category_id == category).paginate(page=page, per_page=per_page)
            return render_template("auctions.html", auctions=auctions, categories=categories)

        auctions = query.paginate(page=page, per_page=per_page)
        return render_template("auctions.html", auctions=auctions, categories=categories)

    if category:
        query = query.join(Auction.item)
        filters.append(Item.category_id == category)   # save the boolean expression
        
    if situation:
        filters.pop(0)
        filters.append(Auction.situation == situation)

    if filters:
        # unpack the filters list, each element(expression) it's passed as an argument
        query = query.filter(*filters)

    # return a piece of registers
    auctions = query.paginate(page=page, per_page=per_page)   # return an object
    # items is an attribute of auctions. Which is a list that contains objects, in this case the obj Auction
    data = [{"id": a.auction_id, "name": a.item.name, "end_date": a.end_date, "value":
            a.buy_now, "image": a.item.url_image}
            for a in auctions.items]
    
    # Return a json, because the browser and JS don't understand python objects
    return jsonify({
        "auctions": data,
        "has_next": auctions.has_next,
        "has_prev": auctions.has_prev,
        "page": auctions.page,
        "total_pages": auctions.pages
    })


# The first acess
@auctions_bp.route("/auctions")
def list_auctions():
    page = request.args.get("page", 1, type=int)
    per_page = 16
    category = request.args.get("category", type=int)
    situation = request.args.get("situation")

    categories = Category.query.all()

    # show the active auctions as standard
    filters = [Auction.situation == "active"]    # will store the boolean expressions
    query = Auction.query


    # Show all auctions
    if situation == "all":
        # if the user selected some category
        if category:
            auctions = query.join(Auction.item).filter(Item.category_id == category).paginate(page=page, per_page=per_page)
            return render_template("auctions.html", auctions=auctions, categories=categories)

        auctions = query.paginate(page=page, per_page=per_page)
        return render_template("auctions.html", auctions=auctions, categories=categories)

    if category:
        query = query.join(Auction.item)
        filters.append(Item.category_id == category)   # save the boolean expression
        
    # other auction's situation
    if situation:
        filters.pop(0)   # remove the standard case
        filters.append(Auction.situation == situation)

    if filters:
        # unpack the filters list, each element(expression) it's passed as an argument
        query = query.filter(*filters)


    auctions = query.paginate(page=page, per_page=per_page)

    # Render the first page with jinja
    return render_template("auctions.html", auctions=auctions, categories = categories)
