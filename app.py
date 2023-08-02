from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.category import Category
from models.product import Product, Price, Grade, Review
from database import Database

app = Flask(__name__)
cartLengthExample = 5


@app.route('/')
def home():
    db = Database('database.db')
    categories = Category.get_all_categories(db)
    recommended_products = Product.get_promotion_products(db)
    return render_template(
        'index.html',
        categories=categories,
        cartLength=cartLengthExample,
        recommended_products=recommended_products
    )


@app.route('/products')
def products(custom_product_list=None):
    db = Database('database.db')
    categories = Category.get_all_categories(db)

    return render_template(
        'products.html',
        categories=categories,
        cartLength=cartLengthExample,
        products=custom_product_list if custom_product_list else Product.get_all_products(db)
    )


@app.route('/detail')
def detail():
    db = Database('database.db')
    product_id = int(request.args.get('id'))
    product = Product.get_product_by_id(db, product_id)

    if not product:
        return redirect(url_for('home'))

    product.reviews = Review.get_reviews_by_product_id(db, product_id)
    product.grade = product.calculate_product_grade(product.reviews)
    categories = Category.get_all_categories(db)

    return render_template(
        'detail.html',
        categories=categories,
        cartLength=cartLengthExample,
        product=product
    )


@app.route('/search', methods=['GET'])
def search():
    db = Database('database.db')
    return render_template('mobile-search.html')


@app.route('/search', methods=['POST'])
def search_post():
    db = Database('database.db')
    search_query = request.form['search'].strip()
    products_list = Product.search_products_by_string(db, search_query)
    if not products_list:
        # todo: tornar o no results uma pagina e incluir quando tbm não encontra a id do produto
        return render_template(
            'no-results.html',
            search_query=search_query
        )
    return products(products_list)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return 'Place holder for register.'


@app.route('/register/validation')
def register_validation():
    return 'Place holder for register validation.'


@app.route('/cart')
def cart():
    return 'Place holder for cart.'



