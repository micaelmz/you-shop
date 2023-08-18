from flask import Flask, render_template, redirect
from utils.database import db
from api import api_blueprint

from models.category import Category
from models.product import Product

from routes.detail_bp import detail_blueprint
from routes.user_bp import user_blueprint
from routes.product_bp import product_blueprint
from routes.no_results_bp import no_results_blueprint


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(product_blueprint, url_prefix='/product')
app.register_blueprint(detail_blueprint, url_prefix='/detail')
app.register_blueprint(no_results_blueprint, url_prefix='/no-results')


@app.route('/')
def home():
    return render_template(
        'index.html',
        categories=Category.get_all(),
        cartLength=2,
        recommended_products=Product.get_on_sale_products()
    )


@app.route('/api/docs')
def api_docs():
    return redirect('https://documenter.getpostman.com/view/29096336/2s9Xy5LA6U?version=latest')
