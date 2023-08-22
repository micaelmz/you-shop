from flask import render_template, url_for, redirect, request
from models.product import Product


# todo: páginaçõa
def base_products(products_list, search_query=None):
    return render_template(
        'products.html',
        products=products_list,
        search_query=search_query  # exibido no título da página quando há uma busca
    )


def all_products():
    products_list = Product.get_all()
    return base_products(products_list)


def products_by_category(category_id):
    products_list = Product.get_products_by_category_id(category_id)

    if not products_list:
        return redirect(url_for('no_results.category', category_id=category_id))

    return base_products(products_list)


def search_page():
    return render_template('mobile-search.html')


# todo: existe essa diferença entre search_form e search_products pq o form é um POST e o search_products é um GET, tentar unificar
def search_form():
    search_query = request.form['search'].strip()
    return redirect(url_for('product.search_products', search_query=search_query))


def search_products(search_query):
    products_list = Product.search_products_by_string(search_query.strip())

    if not products_list:
        return redirect(url_for('no_results.search', search_query=search_query))

    return base_products(products_list, search_query)
