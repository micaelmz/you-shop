from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.category import Category
from models.product import Product, Price, Grade, Review
from database import Database

app = Flask(__name__)
cartLengthExample = 0


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
def products():
    # TODO: refatorar essa bagunça de rota
    db = Database('database.db')
    categories = Category.get_all_categories(db)

    search_query = request.args.get('search')
    category_id = request.args.get('category')
    page = int(request.args.get('page', 1))  # Default to page 1 if 'page' parameter is not provided
    page_size = 6  # MMC entre 2(quantidade de colunas mobile) e 3 (quantidade de colunas desktop)

    if search_query:
        products_list = Product.search_products_by_string(db, search_query.strip())
        if not products_list:
            return render_template(
                'no-results.html',
                search_query=search_query
            )
    elif category_id:
        products_list = Product.get_products_by_category_id(db, int(category_id))
        if not products_list:
            return render_template(
                'no-results.html',
                search_query=f"Categoria {Category.get_category_by_id(db, int(category_id)).name}"
            )
    else:
        products_list = Product.get_all_products(db)

    # Implement pagination using list slices
    total_items = len(products_list)  # 6
    start_index = (page - 1) * page_size  # 0
    end_index = start_index + page_size  # 6
    products_list = products_list[start_index:end_index]
    total_pages = total_items // page_size + (1 if total_items % page_size > 0 else 0)

    if start_index >= total_items:
        if search_query:
            warning_text = f"página {page} da busca '{search_query}'"
        elif category_id:
            warning_text = f"página {page} da categoria {Category.get_category_by_id(db, int(category_id)).name}"
        else:
            warning_text = f"página {page}"
        return render_template(
            'no-results.html',
            search_query=warning_text
        )

    return render_template(
        'products.html',
        categories=categories,
        cartLength=cartLengthExample,
        products=products_list,
        current_page=page,
        total_pages=total_pages,
        search_query=search_query,
        category_id=int(category_id) if category_id else None
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
    return redirect(url_for('products', search=request.form['search']))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register/validation')
def register_validation():
    return 'Place holder for register validation.'


@app.route('/cart')
def cart():
    return 'Place holder for cart.'
