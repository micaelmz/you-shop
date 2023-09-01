from flask import render_template
from flask_login import login_required, current_user
from models.cart import Cart


@login_required
def cart():
    return render_template(
        'cart.html',
    )


@login_required
def add_to_cart(product_id, qnt):
    new_cart = Cart(
        user_id=current_user.id,
        product_id=product_id,
        qnt=qnt
    )
