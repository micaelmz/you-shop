from colorthief import ColorThief
import requests
import datetime

class Grade:
    def __init__(self, grade):
        self.grade = grade
        self.integer = int(grade)
        self.decimal = int(round((grade - self.integer) * 10))

    def __str__(self):
        return f"{self.integer},{self.decimal}"


class Price:
    def __init__(self, new, old):
        self.new = new
        self.old = old

    def __str__(self):
        return self.format_price(self.new)

    def format_price(self, price):
        return "{:.2f}".format(price)


class Review:
    def __init__(self, id, author_id, product_id, content, grade, date, author_name=None):
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
    def get_all_reviews(db):
        try:
            db.cursor.execute('SELECT * FROM review')
            rows = db.cursor.fetchall()
            reviews = []
            for row in rows:
                reviews.append(Review(*row))
            return reviews
        except Exception as e:
            raise e

    @staticmethod
    def get_product_reviews(cursor, product_id):
        cursor.execute('SELECT * FROM review WHERE product_id = ?', (product_id,))
        rows = cursor.fetchall()
        reviews = []
        for row in rows:
            reviews.append(Review(*row))
        return reviews

    @staticmethod
    def commit_review(db, review: object) -> int:
        try:
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
        except Exception as e:
            raise e

    @staticmethod
    def delete_review(db, review_id) -> int:
        try:
            db.cursor.execute('DELETE FROM review WHERE id = ?', (review_id,))
            db.conn.commit()
            return db.cursor.rowcount
        except Exception as e:
            raise e



class Product:
    def __init__(self, id, name, price, price_old, category, promotion,
                 image_url, description, reviews=None, color=None):
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
        self.color = color if color else self.detect_color()

    def __str__(self):
        return f"{self.name} - {self.price}"

    def detect_color(self) -> str:
        # raw_img = requests.get(self.image_thumb, stream=True).raw
        # color_thief = ColorThief(raw_img)
        # dominant_color = color_thief.get_color(quality=1)
        dominant_color = 'Neutro'
        return dominant_color

    def calculate_product_grade(self, reviews: list) -> Grade:
        if len(reviews) == 0:
            return Grade(0)
        grades = [review.grade.grade for review in reviews]
        return Grade(sum(grades) / len(grades))

    @staticmethod
    def get_all_products(cursor: object) -> list[object]:
        cursor.execute('SELECT * FROM product')
        rows = cursor.fetchall()
        products = []
        for row in rows:
            products.append(Product(*row))
        return products

    @staticmethod
    def send_product(cursor, product: object) -> int:
        cursor.execute('INSERT INTO product VALUES (?,?,?,?,?,?,?,?,?)', (
            product.id,
            product.name,
            product.price.new,
            product.price.old,
            product.category,
            product.promotion,
            product.image_thumb,
            product.description,
            product.color
        ))
        cursor.conn.commit()
        return cursor.lastrowid


if __name__ == '__main__':
    from database import Database
    review = Review.get_all_reviews(Database('../database.db').create_cursor())
    for r in review:
        print(r)
