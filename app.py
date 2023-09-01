from flask import render_template, redirect, Flask
from flask_login import LoginManager

from api import api_blueprint
from utils.database import db

from models.cart import Cart
from models.category import Category
from models.product import Product, Price
from models.user import User

from routes.detail_bp import detail_blueprint
from routes.user_bp import user_blueprint
from routes.product_bp import product_blueprint
from routes.no_results_bp import no_results_blueprint
from routes.auth_bp import auth_blueprint

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.pre_login'

# with app.app_context():
#     db.create_all()

app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(product_blueprint, url_prefix='/product')
app.register_blueprint(detail_blueprint, url_prefix='/detail')
app.register_blueprint(no_results_blueprint, url_prefix='/no-results')
app.register_blueprint(auth_blueprint, url_prefix='/auth')


# Injetando categorias no contexto de todas as rotas
@app.context_processor
def inject_categories():
    return dict(categories=Category.get_all())


@app.template_global()
def label_price(price: float) -> str:
    return Price.label_price(price)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route('/')
def home():
    return render_template(
        'index.html',
        recommended_products=Product.get_on_sale_products()
    )


@app.route('/api/docs')
def api_docs():
    return redirect('https://documenter.getpostman.com/view/29096336/2s9Xy5LA6U?version=latest')


@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms-of-service.html')


@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')
