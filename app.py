from flask import Flask
from controller.toggle_theme import theme_bp
from controller import register_routes
from models.db import db
from models.category import Category
import secrets
import os
from dotenv import load_dotenv
from controller.verify_login import login_required
from scheduler.scheduler import scheduler
from scheduler.jobs import check_expired_auctions, check_scheduled_auctions
from errors.errors import register_error_handlers
from socketio_instance import socketio

load_dotenv()

app = Flask(__name__)

socketio.init_app(app)

# Secret key
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

if not app.config["SQLALCHEMY_DATABASE_URI"]:
    raise RuntimeError("DATABASE URL não configurada.")

db.init_app(app)

# Default categories
default_categories = ["Eletrônicos", "Roupas", "Móveis", "Livros", "Jogos"]

with app.app_context():

    # Create tables
    db.create_all()

    # Insert default categories if they don't exist
    for cat_name in default_categories:
        exists = Category.query.filter_by(name=cat_name).first()
        if not exists:
            db.session.add(Category(name=cat_name))

    db.session.commit()

# Register routes and middlewares
register_routes(app)
login_required(app)
register_error_handlers(app)

# Start scheduler and periodic jobs
def start_scheduler():

    if not scheduler.running:

        scheduler.start()

        # Check auctions that should end
        scheduler.add_job(
            func=check_expired_auctions,
            trigger="interval",
            seconds=30,
            id="check_expired_auctions",
            replace_existing=True
        )

        # Check auctions that should start
        scheduler.add_job(
            func=check_scheduled_auctions,
            trigger="interval",
            seconds=30,
            id="check_scheduled_auctions",
            replace_existing=True
        )

start_scheduler()

if __name__ == "__main__":
    socketio.run(app)