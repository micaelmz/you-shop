from flask import render_template, url_for, redirect, request
from models.category import Category
from models.product import Product
from models.review import Review


# todo: páginaçõa
def products(products_list):
    return render_template(
        'products.html',
        cartLength=0,
        categories=Category.get_all(),
        products=products_list
    )


def all_products():
    products_list = Product.get_all()
    return products(products_list)


def products_by_category(category_id):
    products_list = Product.get_products_by_category_id(category_id)
    return products(products_list)


def search_page():
    return render_template('mobile-search.html')


def search_form():
    search_query = request.form['search_query']
    return search_products(search_query)


def search_products(search_query):
    products_list = Product.search_products_by_string(search_query.strip())

    if not products_list:
        return redirect(url_for('no_results.search', search_query=search_query))

    return products(products_list)
