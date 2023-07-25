from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.category import Category
from models.product import Product, Price, Grade, Review

app = Flask(__name__)

cartLengthExample = 5
categoriesExample = [
    Category(1, 'Feminino'),
    Category(2, 'Masculino'),
    Category(3, 'Infantil'),
    Category(4, 'Acessórios'),
    Category(5, 'Teste'),
]
productExample = Product(
    id=1,
    name='Vestido Azul tentando quebrar a pagina escrevenmdo um nome mto grande oi 123',
    price=50,
    price_old=100,
    category=1,
    image_url='https://cdn.awsli.com.br/1500x1500/67/67661/produto/206450249/whatsapp-image-2023-03-02-at-15-42-09-oswmhm.jpg',
    description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl sed tincidunt ultricies, nunc nisl luctus nunc, nec aliquam nisl nunc v',
    reviews=[
            Review(1, 'João', 'Muito bom', 4.9),
            Review(2, 'Maria', 'legal', 4),
            Review(3, 'José', 'lixo', 1),
            Review(4, 'João', 'bom', 3),
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
