from flask import Flask
from controller.toggle_theme import theme_bp
from controller import register_routes
from models.db import db
import secrets
import os
from dotenv import load_dotenv
from controller.verify_login import login_required
from scheduler.scheduler import scheduler
from scheduler.jobs import close_auction
from errors.errors import register_error_handlers

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


register_routes(app)
login_required(app)
register_error_handlers(app)

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

start_scheduler()

if __name__ == "__main__":
    app.run()