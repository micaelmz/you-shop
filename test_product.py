import pytest
from models.product import Grade, Price, Review, Product
from database import Database
import datetime

# todo: criar DDL para o mock do banco de dados, para que os testes não dependam do arquivo test_db.db
db = Database('test_db.db')
test_reviews = [
    Review(id=1, author_id=1, product_id=1, content="Good",
           grade=4.0, date="01-01-2021", author_name="User1"
           ),
    Review(id=2, author_id=2, product_id=1, content="Excellent",
           grade=4.8, date="01-01-2021", author_name="User2"
           ),
    Review(id=3, author_id=3, product_id=1, content="Average",
           grade=3.5, date="01-01-2021", author_name="User3"
           )
]


def test_grade_str():
    grade = Grade(3.2)
    assert str(grade) == "3,2"


# Test Price class
def test_price_format_price():
    price = Price(25.99, 15.5)
    assert price.format_price(25.99) == "25.99"
    assert price.format_price(15.5) == "15.50"


def test_price_str():
    price = Price(29.95, 20.0)
    assert str(price) == "29.95"


# Test Review class
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


# Test Product class
def test_product_detect_color():
    pass


def test_product_calculate_grade():
    product_test1 = Product(id=1, name="Test Product", price=25.99, price_old=50.0, category='Test Category',
                           promotion=False, image_url='https://www.test.com/test.jpg', description='Test Description',
                           reviews=test_reviews)
    assert str(product_test1.grade) == "4,1"
    product_test2 = Product(id=2, name="Test Product", price=25.99, price_old=50.0, category='Test Category',
                            promotion=False, image_url='https://www.test.com/test.jpg', description='Test Description')
    assert str(product_test2.grade) == "0,0"
