from flask import Flask

# Function that register all the blueprints
def register_routes(app: Flask):
    from .home import home_bp
    from .login import login_bp
    from .register import register_bp
    from .logout import logout_bp
    from .page import page_bp
    from .perfil import perfil_bp, perfil_info_bp
    from .toggle_theme import theme_bp
    from .list_auctions import api_auctions_bp, auctions_bp
    from .item import item_bp
    from .register_item import register_item_bp
    from .categories import categories_bp
    from .sell import sell_bp, api_item_bp
    from .public_auction import public_auction_bp
    from .balance import balance_bp
    from .items import items_bp, item_info_bp
    from .auction import auction_bp
    from .recharge import recharge_bp
    from .update_info import update_basic_info_bp, update_password_bp
    from .complete_register import complete_register_bp
    from .bid import bid_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(page_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(perfil_info_bp)
    app.register_blueprint(theme_bp)
    app.register_blueprint(api_auctions_bp)
    app.register_blueprint(auctions_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(register_item_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(sell_bp)
    app.register_blueprint(api_item_bp)
    app.register_blueprint(public_auction_bp)
    app.register_blueprint(balance_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(item_info_bp)
    app.register_blueprint(auction_bp)
    app.register_blueprint(recharge_bp)
    app.register_blueprint(update_basic_info_bp)
    app.register_blueprint(update_password_bp)
    app.register_blueprint(complete_register_bp)
    app.register_blueprint(bid_bp)