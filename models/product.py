from colorthief import ColorThief
import requests
import datetime
from database import Database, db_handler
import json
from typing import Dict


# TODO: usar pydantic para validar os dados
# TODO: usar SQLAlchemy para fazer o mapeamento objeto-relacional


class Grade:
    def __init__(self, grade: float):
        self.grade = grade
        self.integer = int(grade)
        self.decimal = int(round((grade - self.integer) * 10))

    def __str__(self):
        return f"{self.integer},{self.decimal}"


class Price:
    def __init__(self, new: float, old: float):
        self.new = new
        self.old = old

    def __str__(self):
        return self.format_price(self.new)

    @staticmethod
    def format_price(price) -> str:
        return "{:.2f}".format(price).replace('.', ',')


class Review:
    def __init__(self, id: int, author_id: int, product_id: int, content: str, grade: float, date: str,
                 author_name=None):
        self.id = id
        self.author_id = author_id
        self.product_id = product_id
        self.content = content
        self.grade = Grade(grade)
        self.date = datetime.datetime.strptime(date, '%d-%m-%Y')
        self.author_name = author_name

    def __str__(self):
        return f"{self.author_name}: {self.content} ({self.grade})"

    @staticmethod
    @db_handler
    def get_all_reviews(db: Database) -> list['Review']:
        db.cursor.execute('SELECT * FROM review')
        rows = db.cursor.fetchall()
        reviews = []
        for row in rows:
            reviews.append(Review(*row))
        return reviews

    @staticmethod
    @db_handler
    def get_reviews_by_product_id(db: Database, product_id: int) -> list['Review']:
        db.cursor.execute('SELECT * FROM review WHERE product_id = ?', (product_id,))
        rows = db.cursor.fetchall()
        reviews = []
        for row in rows:
            reviews.append(Review(*row))
        return reviews

    @staticmethod
    @db_handler
    def commit_review(db: Database, review: 'Review') -> int:
        db.cursor.execute('INSERT INTO review VALUES (?,?,?,?,?,?, ?)', (
            review.id,
            review.author_id,
            review.product_id,
            review.content,
            review.grade.grade,
            review.date.strftime('%d-%m-%Y'),
            review.author_name
        ))
        db.conn.commit()
        return db.cursor.lastrowid

    @staticmethod
    @db_handler
    def delete_review(db: Database, review_id: int) -> int:
        db.cursor.execute('DELETE FROM review WHERE id = ?', (review_id,))
        db.conn.commit()
        return db.cursor.rowcount


class Product:
    def __init__(self, id: int, name: str, price: float, price_old: float, category: str, promotion: bool,
                 image_url: str, description: str, color=None, add_info: str = None, reviews=None):
        self.id = id
        self.name = name
        # todo: receber o price como um objeto Price
        self.price = Price(price, price_old)
        self.category = category
        self.promotion = promotion
        self.image_thumb = image_url
        self.extra_images = []
        self.description = description
        self.reviews = reviews if reviews else []
        self.grade = self.calculate_product_grade(self.reviews)
        self.color = color if color else self.detect_color(self.image_thumb)
        self.additional_info = json.loads(add_info) if add_info else None

    def __str__(self):
        return f"{self.name} - {self.price}"

    @staticmethod
    def calculate_product_grade(reviews: list['Review']) -> Grade:
        if len(reviews) == 0:
            return Grade(0)
        grades = [review.grade.grade for review in reviews]
        return Grade(sum(grades) / len(grades))

    @staticmethod
    def detect_color(img_url: str) -> str:
        # raw_img = requests.get(self.image_thumb, stream=True).raw
        # color_thief = ColorThief(raw_img)
        # dominant_color = color_thief.get_color(quality=1)
        dominant_color = 'Neutro'
        return dominant_color

    @staticmethod
    @db_handler
    def get_all_products(db: Database) -> list['Product']:
        db.cursor.execute('SELECT * FROM product')
        rows = db.cursor.fetchall()
        products = []
        for row in rows:
            products.append(Product(*row))
        return products

    @staticmethod
    @db_handler
    def get_promotion_products(db: Database) -> list['Product']:
        db.cursor.execute('SELECT * FROM product WHERE promotion = 1')
        rows = db.cursor.fetchall()
        products = []
        for row in rows:
            products.append(Product(*row))
        return products

    @staticmethod
    @db_handler
    def get_product_by_id(db: Database, product_id: int) -> 'Product':
        db.cursor.execute('SELECT * FROM product WHERE id = ?', (product_id,))
        row = db.cursor.fetchone()
        return Product(*row)

    @staticmethod
    @db_handler
    def commit_product(db: Database, product: 'Product') -> int:
        db.cursor.execute('INSERT INTO product VALUES (?,?,?,?,?,?,?,?,?,?)', (
            product.id,
            product.name,
            product.price.new,
            product.price.old,
            product.category,
            product.promotion,
            product.image_thumb,
            product.description,
            "",  # product.color
            product.additional_info
        ))
        db.conn.commit()
        return db.cursor.lastrowid

    @staticmethod
    @db_handler
    def delete_product(db: Database, product_id: int) -> int:
        db.cursor.execute('DELETE FROM product WHERE id = ?', (product_id,))
        db.conn.commit()
        return db.cursor.rowcount

if __name__ == '__main__':
    db = Database('../database.db')
    product = Product.get_product_by_id(db, 2)
    for key, value in product.additional_info.items():
        print(f"{key}: {value}")

