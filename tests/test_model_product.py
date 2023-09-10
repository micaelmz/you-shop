from flask_testing import TestCase
import pytest
import sys
import os
from flask import Flask

if not __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.product import Product, Price
from utils.database import db


class TestModels(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.init_app(app)

        self.db = db
        self.app = app

        with self.app.app_context():
            self.db.create_all()

        return app

    def setUp(self):
        product1 = Product(
            name="Test Product 1",
            category_id=1,
            price_current=25.99,
            price_old=30,
            on_sale=True,
            image="https://via.placeholder.com/200x200",
            description="Test Product 1 Description",
            color="Red",
            additional_info={"key": "value"},
            additional_images=["https://via.placeholder.com/200x200", "https://via.placeholder.com/200x200"],
        )
        self.db.session.add(product1)
        self.db.session.commit()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_product_name(self):
        product = Product.get_by_id(1)
        assert str(product) == "Test Product 1 - 25,99 (0,0)"


if __name__ == '__main__':
    pytest.main()
