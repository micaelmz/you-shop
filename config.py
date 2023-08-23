import os
from flask import Flask
from flask_login import LoginManager
from utils.database import db
from models.category import Category
from models.product import Price

app = Flask(__name__)
app.config['basedir'] = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.pre_login'


# Injetando categorias no contexto de todas as rotas
@app.context_processor
def inject_categories():
    return dict(categories=Category.get_all())


@app.template_global()
def label_price(price: float) -> str:
    return Price.label_price(price)


with app.app_context():
    db.create_all()
