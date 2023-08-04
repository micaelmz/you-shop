import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from models.review import Review, Grade
from mock_data import test_reviews, test_products, db
from database import Database
import datetime


def test_grade_str():
    grade = Grade(3.2)
    assert str(grade) == "3,2"


def test_product_calculate_grade():
    assert str(test_products[0].grade) == "4,1"
    assert str(test_products[1].grade) == "0,0"


def test_review_initial_values():
    review = test_reviews[0]
    assert review.id == 1
    assert review.author_id == 1
    assert review.product_id == 1
    assert review.content == "Good"
    assert review.author_name == "User1"


def test_review_subobject_values():
    review = test_reviews[0]
    assert type(review.grade) == Grade
    assert review.grade.integer == 4
    assert review.grade.decimal == 0
    assert type(review.date) == datetime.datetime
    assert review.date.year == 2021
    assert review.date.month == 1
    assert review.date.day == 1


def test_review_str():
    review = test_reviews[0]
    assert str(review) == "User1: Good (4,0)"


# Test Review database related operations
def test_commit_review():
    first = Review.commit_review(db, test_reviews[0])
    assert first == 1
    second = Review.commit_review(db, test_reviews[1])
    assert second == 2
    third = Review.commit_review(db, test_reviews[2])
    assert third == 3


def test_get_committed_reviews():
    reviews = Review.get_all_reviews(db)
    assert len(reviews) == len(test_reviews)

    for i in range(len(reviews)):
        assert str(reviews[i]) == str(test_reviews[i])


def test_delete_reviews():
    first = Review.delete_review(db, test_reviews[0].id)
    assert first == 1
    second = Review.delete_review(db, test_reviews[1].id)
    assert second == 1
    third = Review.delete_review(db, test_reviews[2].id)
    assert third == 1
