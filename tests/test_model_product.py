from flask_testing import TestCase
import pytest
import sys
import os
from flask import Flask

if not __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mock_data import *
from models.product import Product, Price
from database import db


class TestModels(TestCase):
    def create_app(self):
        if os.path.exists("test.db"):
            os.remove("test.db")
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.init_app(app)
        with app.app_context():
            db.create_all()
        return app

    def test_price_format_price(self):
        price = Price(25.99, 15.5)
        assert price.label_price(25.99) == "25,99"
        assert price.label_price(15.5) == "15,50"

    def test_price_str(self):
        price = Price(29.95, 20.0)
        assert str(price) == "29,95"

    def test_product_detect_color(self):
        pass

    def test_commit_product(self):
        first = test_products[0].commit()
        assert first == 1
        second = test_products[1].commit()
        assert second == 2

    def test_get_all_product(self):
        products = Product.get_all_products()
        assert len(products) != 0
        assert len(products) == len(test_products)

    def test_get_product_by_id(self):
        product = Product.get_product_by_id(1)
        assert product.name == "Test Product"

    def test_more_information_json(self):
        pass


if __name__ == '__main__':
    pytest.main()
