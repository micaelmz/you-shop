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


@app.route('/login')
def login():
    return 'Place holder'


@app.route('/register')
def register():
    return 'Place holder'


@app.route('/cart')
def cart():
    return 'Place holder'


@app.route('/products')
def products():
    db = Database('database.db')
    products = Product.get_all_products(db)
    categories = Category.get_all_categories(db)
    return render_template(
        'products.html',
        categories=categories,
        cartLength=cartLengthExample,
        products=products
    )


@app.route('/detail')
def detail():
    db = Database('database.db')
    product_id = int(request.args.get('id'))
    product = Product.get_product_by_id(db, product_id)

    if not product:
        return redirect(url_for('home'))

    product.reviews = Review.get_review_by_product_id(db, product_id)
    product.grade = product.calculate_product_grade(product.reviews)
    categories = Category.get_all_categories(db)

    return render_template(
        'detail.html',
        categories=categories,
        cartLength=cartLengthExample,
        product=product
    )


if __name__ == '__main__':
    app.run(debug=True)
