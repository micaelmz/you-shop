from flask import render_template
from models.category import Category


def no_results(message):
    return render_template(
        'no-results.html',
        categories=Category.get_all(),
        cartLength=5,
        message=message
    )


def product(product_id):
    return no_results(f'produto ID: "{product_id}"')


def category(category_id):
    aimed_category = Category.get_by_id(category_id)
    if aimed_category:
        return no_results(f'produtos da categoria: "{aimed_category.name}"')
    return no_results(f'categoria inexistente ID: "{category_id}"')


def search(search_query):
    return no_results(f'busca: "{search_query}"')
