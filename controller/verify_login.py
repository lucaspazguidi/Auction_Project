from flask import Flask, redirect, url_for, session, request

def login_required(app: Flask):
    @app.before_request
    def verify_login():
        open_routes = ['/' ,'home.home', 'register.register', 'login.login', 'static', 'page.page',
                        'theme.toggle_theme', 'list_auctions.list_auctions', 'categories.categories', 'auction.auction']

        # The route is public and don't need login
        if request.endpoint in open_routes:
            return None
        
        # Verify if the cookie exist, if so, re-assign the session values and allows the user to acess the route
        if "user_id" not in session:
            cookie_logged = request.cookies.get("user_id")
            if cookie_logged:
                session["user_id"] = int(cookie_logged)
                session["logged"] = True
                return None
            else:
                return redirect(url_for("login.login"))

       