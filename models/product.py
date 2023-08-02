from database import Database, db_handler
import json
from models.review import Review, Grade

# TODO: usar pydantic para validar os dados
# TODO: usar SQLAlchemy


class Price:
    def __init__(self, new: float, old: float):
        self.new = new
        self.old = old

    def __str__(self):
        return self.format_price(self.new)

    @staticmethod
    def format_price(price) -> str:
        return "{:.2f}".format(price).replace('.', ',')


class Product:
    def __init__(self, id: int, name: str, price: float, price_old: float, category: str, promotion: bool,
                 image_url: str, description: str, color=None, add_info: str = None, extra_img: str = None, reviews=None):
        self.id = id
        self.name = name
        # todo: receber o price como um objeto Price
        self.price = Price(price, price_old)
        self.category = category
        self.promotion = promotion
        self.image_thumb = image_url
        self.description = description
        self.reviews = reviews if reviews else []
        self.grade = self.calculate_product_grade(self.reviews)
        self.color = color if color else self.detect_color(self.image_thumb)
        self.additional_info = json.loads(add_info) if add_info else None
        self.extra_images = json.loads(extra_img) if extra_img else {}

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
        db.cursor.execute('INSERT INTO product VALUES (?,?,?,?,?,?,?,?,?,?,?)', (
            product.id,
            product.name,
            product.price.new,
            product.price.old,
            product.category,
            product.promotion,
            product.image_thumb,
            product.description,
            "",  # product.color
            product.additional_info,
            json.dumps(product.extra_images)
        ))
        db.conn.commit()
        return db.cursor.lastrowid

    @staticmethod
    @db_handler
    def delete_product(db: Database, product_id: int) -> int:
        db.cursor.execute('DELETE FROM product WHERE id = ?', (product_id,))
        db.conn.commit()
        return db.cursor.rowcount

    @staticmethod
    @db_handler
    def search_products_by_string(db: Database, search_string: str) -> list['Product']:
        db.cursor.execute(
            "SELECT * FROM product WHERE LOWER(name) LIKE LOWER(?) OR LOWER(description) LIKE LOWER(?)",
            ('%' + search_string + '%', '%' + search_string + '%'))
        rows = db.cursor.fetchall()
        products = []
        for row in rows:
            products.append(Product(*row))
        return products

    @staticmethod
    @db_handler
    def get_products_by_category_id(db: Database, category: int) -> list['Product']:
        db.cursor.execute('SELECT * FROM product WHERE category = ?', (category,))
        rows = db.cursor.fetchall()
        products = []
        for row in rows:
            products.append(Product(*row))
        return products


if __name__ == '__main__':
    db = Database('../database.db')
    product = Product.get_product_by_id(db, 2)
    for key, value in product.additional_info.items():
        print(f"{key}: {value}")

