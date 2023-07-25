import pytest
from models.product import Grade, Price, Review, Product

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
def test_review_init():
    review = Review(1, "John Doe", "Great product!", 4.8)
    assert review.id == 1
    assert review.author == "John Doe"
    assert review.content == "Great product!"
    assert str(review.grade) == "4,8"


def test_review_str():
    review = Review(1, "Jane Doe", "Nice item!", 3.2)
    assert str(review) == "Jane Doe: Nice item!"


# Test Product class
def test_product_detect_color():
    # This test requires mocking the requests.get() method or using a valid image URL.
    # Replace 'https://cdn.awsli.com.br/1500x1500/67/67661/produto/206450249/whatsapp-image-2023-03-02-at-15-42-09-oswmhm.jpg' with a real image URL for testing.
    product = Product(1, "Test Product", 25.99, "Category",
                      "https://cdn.awsli.com.br/1500x1500/67/67661/produto/206450249/whatsapp-image-2023-03-02-at-15-42-09-oswmhm.jpg",
                      "Product description", [])
    assert product.detect_color() == (199, 199, 197)


def test_product_calculate_grade():
    reviews = [
        Review(1, "User1", "Good", 4.0),
        Review(2, "User2", "Excellent", 4.8),
        Review(3, "User3", "Average", 3.5)
    ]
    product = Product(1, "Test Product", 25.99, "Category",
                      "https://cdn.awsli.com.br/1500x1500/67/67661/produto/206450249/whatsapp-image-2023-03-02-at-15-42-09-oswmhm.jpg",
                      "Product description", reviews)
    assert str(product.grade) == "4,1"