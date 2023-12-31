from flask import render_template, redirect, Flask, session
from flask_login import LoginManager

from api import api_blueprint
from utils.database import db
from utils.mail import mail, send_email, send_confirmation_code

from models import Cart, Category, Product, Review, User, Price
from routes import auth_blueprint, no_results_blueprint, product_blueprint, user_blueprint

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.pre_login'
mail.init_app(app)

# with app.app_context():
#     db.create_all()

app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(product_blueprint, url_prefix='/product')
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
    showed_disclaimer = session.get('showed_disclaimer', False)
    if not showed_disclaimer:
        session['showed_disclaimer'] = True
    return render_template(
        'index.html',
        recommended_products=Product.get_on_sale_products(),
        showed_disclaimer=showed_disclaimer
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


@app.route('/detail/id/<int:product_id>')
def detail_moved(product_id: int):
    return redirect(f'/product/id/{product_id}', code=301)


@app.route('/send-confirm')
def send_confirm():
    return send_confirmation_code('123456')
