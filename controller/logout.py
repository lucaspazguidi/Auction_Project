from flask import Flask, session, Blueprint, redirect, url_for, make_response

logout_bp = Blueprint("logout", __name__)

@logout_bp.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    session.clear()
    resp.delete_cookie("user_id")
    return resp