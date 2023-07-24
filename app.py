from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.category import Category
from models.product import Product

app = Flask(__name__)

cartLengthExample = 11
categoriesExample = [
    Category(1, 'Laptop'),
    Category(2, 'Desktop'),
    Category(3, 'Phone'),
    Category(4, 'Tablet'),
    Category(5, 'Watch'),
    Category(6, 'TV'),
    Category(7, 'Camera'),
    Category(8, 'Printer'),
    Category(9, 'Headphone'),
    Category(10, 'Speaker'),
    Category(11, 'Monitor'),
    Category(12, 'Keyboard'),
    Category(13, 'Mouse'),
]

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

@app.route('/detail')
def detail():
    return render_template(
        'detail.html',
        categories=categoriesExample,
        cartLength=cartLengthExample,
    )


if __name__ == '__main__':
    app.run(debug=True)
