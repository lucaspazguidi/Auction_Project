from flask import Blueprint, render_template, abort, session, redirect, url_for

page_bp = Blueprint("page", __name__)

PAGES = ["home", "about", "blog", "categories", "contact",
        "faq", "login", "privacy", "register", "returns", "terms", "promotions"]


@page_bp.route("/page/<page>")
# route that render simple html pages
def page(page):

    if page not in PAGES:
        abort(404)

    return render_template(f"{page}.html")

