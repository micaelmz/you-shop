from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.category import Category
from models.product import Product, Price, Grade, Review
from database import Database

app = Flask(__name__)
cartLengthExample = 5
categoriesExample = [
    Category(1, 'Feminino'),
    Category(2, 'Masculino'),
    Category(3, 'Infantil'),
    Category(4, 'Acessórios'),
    Category(5, 'Teste'),
]
# Todo: necessário chamar o DB, pois a lista productsExample foi deletada para ser substituída pelo mockup do DB

@app.route('/')
def home():
    return 'Place holder'

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
    return render_template(
        'products.html',
        categories=categoriesExample,
        cartLength=cartLengthExample,
        products=products
    )

@app.route('/detail')
def detail():
    db = Database('database.db')
    product_id = int(request.args.get('id'))
    product = Product.get_product_by_id(db, product_id)
    product.reviews = Review.get_review_by_product_id(db, product_id)
    product.grade = product.calculate_product_grade(product.reviews)
    return render_template(
        'detail.html',
        categories=categoriesExample,
        cartLength=cartLengthExample,
        product=product
    )


if __name__ == '__main__':
    app.run(debug=True)
