from flask import Blueprint, render_template, request, redirect, url_for
from models.category import Category
from models.product import Product
import requests

view_blueprint = Blueprint('view', __name__)
cartLengthExample = 0


@view_blueprint.route('/products', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def products():
    if request.method == 'GET':
        pass
    # TODO: refatorar essa bagunça de rota
    # todo: implementar paginação do sqlachemy
    categories = Category.get_all()

    search_query = request.args.get('search')
    category_id = request.args.get('category')
    page = int(request.args.get('page', 1))  # Default to page 1 if 'page' parameter is not provided
    page_size = 6  # MMC entre 2(quantidade de colunas mobile) e 3 (quantidade de colunas desktop)

    if search_query:
        products_list = Product.search_products_by_string(search_query.strip())
        if not products_list:
            return render_template(
                'no-results.html',
                categories=categories,
                cartLength=cartLengthExample,
                search_query=search_query
            )
    elif category_id:
        products_list = Product.get_products_by_category_id(int(category_id))
        if not products_list:
            return render_template(
                'no-results.html',
                categories=categories,
                cartLength=cartLengthExample,
                search_query=f"Categoria {Category.get_by_id(int(category_id)).name}"
            )
    else:
        products_list = Product.get_all()

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
            warning_text = f"página {page} da categoria {Category.get_by_id(int(category_id))}"
        else:
            warning_text = f"página {page}"
        return render_template(
            'no-results.html',
            categories=categories,
            search_query=warning_text,
            cartLength=cartLengthExample
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



@view_blueprint.route('/search', methods=['GET'])
def search():
    return render_template('mobile-search.html')


@view_blueprint.route('/search', methods=['POST'])
def search_post():
    return redirect(url_for('view.products', search=request.form['search']))


@view_blueprint.route('/login')
def login():
    return render_template('login.html')


@view_blueprint.route('/register')
def register():
    return render_template('register.html')


@view_blueprint.route('/register/validation')
def register_validation():
    return 'Place holder for register validation.'


@view_blueprint.route('/cart')
def cart():
    return 'Place holder for cart.'

@view_blueprint.route('/api/docs')
def api_docs():
    return redirect('https://documenter.getpostman.com/view/29096336/2s9Xy5LA6U?version=latest')
