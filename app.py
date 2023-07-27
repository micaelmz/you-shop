from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.category import Category
from models.product import Product, Price, Grade, Review
from database import Database

app = Flask(__name__)
db = Database('database.db')
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

@app.route('/detail')
def detail():
    return render_template(
        'detail.html',
        categories=categoriesExample,
        cartLength=cartLengthExample,
        product=None
    )


if __name__ == '__main__':
    app.run(debug=True)
