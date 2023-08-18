from flask import render_template, request, redirect, url_for
from models.product import Product
from models.category import Category


def product_detail(product_id):
    product = Product.get_by_id(product_id)

    if not product:
        return redirect(url_for('no_results.product', product_id=product_id))

    return render_template(
        'detail.html',
        categories=Category.get_all(),
        cartLength=5,
        product=product
    )
