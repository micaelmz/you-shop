from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.category import Category
from models.product import Product, Price, Grade, Review

app = Flask(__name__)

cartLengthExample = 99
categoriesExample = [
    Category(1, 'Laptop'),
    Category(2, 'Desktop'),
    Category(3, 'Phone'),
    Category(4, 'Tablet'),
    Category(5, 'Watch'),
    Category(6, 'TV'),
    Category(7, 'Camera'),
    Category(8, 'Headphone'),
    Category(9, 'Speaker'),
    Category(10, 'Printer'),
    Category(11, 'Monitor'),
    Category(12, 'Keyboard'),

]
productExample = Product(
    id=1,
    name='Vestido Azul',
    price=200,
    price_old=400,
    category='Feminino',
    image_url='https://cdn.awsli.com.br/1500x1500/67/67661/produto/206450249/whatsapp-image-2023-03-02-at-15-42-09-oswmhm.jpg',
    description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl sed tincidunt ultricies, nunc nisl luctus nunc, nec aliquam nisl nunc v',
    reviews=[
            Review(1, 'João', 'Muito bom', 4.9),
            Review(2, 'Maria', 'legal', 4),
            Review(3, 'José', 'lixo', 1),
        ]
)

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
        product=productExample,
    )


if __name__ == '__main__':
    app.run(debug=True)
