from flask import render_template, request, redirect, url_for
from models.product import Product


def product_detail(product_id):
    product = Product.get_by_id(product_id)
    cart_toast = request.args.get('cart_toast')

    if not product:
        return redirect(url_for('no_results.product', product_id=product_id))

    return render_template(
        'detail.html',
        product=product,
        cart_toast=cart_toast
    )
