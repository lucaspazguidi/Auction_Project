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
from scheduler.jobs import close_auction
from errors.errors import register_error_handlers

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if not app.config["SQLALCHEMY_DATABASE_URI"]:
    raise RuntimeError("DATABASE URL não configurada.")

db.init_app(app)

default_categories = ["Eletrônicos", "Roupas", "Móveis", "Livros", "Jogos"]

with app.app_context():
    db.create_all()
    # Verifica e cria cada categoria se não existir
    for cat_name in default_categories:
        exists = Category.query.filter_by(name=cat_name).first()
        if not exists:
            new_cat = Category(name=cat_name)
            db.session.add(new_cat)
    db.session.commit()

register_routes(app)
login_required(app)
register_error_handlers(app)

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

start_scheduler()

if __name__ == "__main__":
    app.run()