from flask import Flask, render_template
from utils.database import db
from api import api_blueprint
from routes.detail_bp import detail_blueprint
from models.category import Category
from models.product import Product

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

app.register_blueprint(detail_blueprint, url_prefix='/detail')
app.register_blueprint(api_blueprint, url_prefix='/api')


@app.route('/')
def home():
    return render_template(
        'index.html',
        categories=Category.get_all(),
        cartLength=2,
        recommended_products=Product.get_on_sale_products()
    )
