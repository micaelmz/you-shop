import datetime
from database import Database, db_handler


class Grade:
    def __init__(self, grade: float):
        self.grade = grade
        self.integer = int(grade)
        self.decimal = int(round((grade - self.integer) * 10))

    def __str__(self):
        return f"{self.integer},{self.decimal}"


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
