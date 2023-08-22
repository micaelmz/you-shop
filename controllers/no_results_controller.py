from flask import render_template
from models.category import Category


def base_no_results(message):
    return render_template(
        'no-results.html',
        message=message
    )


def product(product_id):
    return base_no_results(f'produto ID: "{product_id}"')


def category(category_id):
    aimed_category = Category.get_by_id(category_id)
    if aimed_category:
        return base_no_results(f'produtos da categoria: "{aimed_category.name}"')
    return base_no_results(f'categoria inexistente ID: "{category_id}"')


def search(search_query):
    return base_no_results(f'busca: "{search_query}"')
