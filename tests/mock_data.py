from models.product import Product
from models.review import Review
from models.category import Category
from models.user import User
from datetime import datetime

test_users = [
    User(
        name="User1"
    ),
    User(
        name="User2"
    ),
    User(
        name="User3"
    )
]

test_categories = [
    Category(
        name="Test Category",
        image="https://www.test.com/test.jpg"
    ),
    Category(
        name="Test Category 2",
        image="https://www.test.com/test2.jpg"
    )
]

test_reviews = [
    Review(
        author_id=1,
        product_id=1,
        content="Good",
        review_grade=4.0,
        date=datetime.now()
    ),
    Review(
        author_id=2,
        product_id=1,
        content="Excellent",
        review_grade=4.8,
        date=datetime.now()
    ),
    Review(
        author_id=3,
        product_id=1,
        content="Average",
        review_grade=3.5,
        date=datetime.now()
    )
]
test_products = [
    Product(
        name="Test Product",
        price_current=25.99,
        price_old=50.0,
        category_id=1,
        promotion=True,
        image='https://www.test.com/test.jpg',
        description='Test Description',
        color='Test Color',
        additional_info={'Test Info': 'Test Value'},
        additional_images={'img1': 'https://www.test.com/test1.jpg'}
    ),
    Product(
        name="Test Product 2",
        price_current=18.0,
        price_old=0,
        category_id=2,
        promotion=False,
        image='https://www.test.com/test.jpg',
        description='Another Test Description',
        color='Test Color 2',
        additional_info={'Second Test Info': 'Second Test Value'},
        additional_images={'img1': 'https://www.test.com/test1.jpg'}
    )
]
