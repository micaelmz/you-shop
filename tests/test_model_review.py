from flask_testing import TestCase
import sys
import os
from flask import Flask

if not __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mock_data import *
from models.review import Review, Rating
from utils.database import db


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

    def setUp(self):
        db.create_all()
        db.session.add_all(test_users)
        db.session.add_all(test_categories)
        db.session.add_all(test_products)
        db.session.commit()

    def test_grade_str(self):
        grade = Rating(3.2)
        assert str(grade) == "3,2"

    def test_commit_review(self):
        first_review = test_reviews[0]
        first_review.commit()
        assert first_review.id == 1
        second_review = test_reviews[1]
        second_review.commit()
        assert second_review.id == 2
        third_review = test_reviews[2]
        third_review.commit()
        assert third_review.id == 3

    def test_product_calculate_rating(self):
        review = Review.get_reviews_by_product_id(1)
        assert len(review) == 3
        product_grade = Rating.calculate_rating_from_reviews(review)
        assert str(product_grade) == "4,1"

    def test_review_initial_values(self):
        review = Review.get_by_id(1)
        assert review.id == 1
        assert review.author_id == 1
        assert review.product_id == 1
        assert review.content == "Good"
        assert review.author_name == "User1"

    def test_review_subobject_values(self):
        now = datetime.now()
        review = Review.get_by_id(1)
        assert type(review.rating) == Rating
        assert review.rating.integer == 4
        assert review.rating.decimal == 0
        assert type(review.date) == datetime
        assert review.date.year == now.year
        assert review.date.month == now.month
        assert review.date.day == now.day

    def test_review_str(self):
        review = Review.get_by_id(1)
        assert str(review) == "User1: Good (4,0)"

