from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.cart import Cart


@login_required
def cart():
    return render_template(
        'cart.html',
    )


@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')
    cart = Cart.get_or_create_cart(current_user.id, product_id)
    cart += int(quantity)
    return redirect(url_for('user.cart'))


@login_required
def delete_item():
    cart_id = request.form.get('cart_id')
    cart = Cart.get_by_id(int(cart_id))
    cart.delete_item()
    return redirect(url_for('user.cart'))
