from models.product import Product
from models.review import Review
from database import Database
import json

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
test_products = [
    Product(
        id=1,
        name="Test Product",
        price=25.99,
        price_old=50.0,
        category='Test Category',
        promotion=False,
        image_url='https://www.test.com/test.jpg',
        description='Test Description',
        reviews=test_reviews,
        additional_info=json.dumps({'Test Info': 'Test Value'}, ensure_ascii=False),
        extra_images=json.dumps({'img1': 'https://www.test.com/test1.jpg'}, ensure_ascii=False)
    ),
    Product(
        id=2,
        name="Test Product 1",
        price=16.99,
        price_old=45.0,
        category='Test Category',
        promotion=True,
        image_url='https://www.test.com/test2.jpg',
        description='Test Description 2',
    )
]
db = Database('tests/mock.db')
db.cursor.executescript(open('tests/mock.sql').read())
