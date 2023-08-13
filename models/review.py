from utils.database import db
from models.user import User
from datetime import datetime


class Grade:
    def __init__(self, grade: float):
        self.grade = grade
        self.integer = int(grade)
        self.decimal = int(round((grade - self.integer) * 10))

    def __str__(self):
        return f"{self.integer},{self.decimal}"

    @staticmethod
    def calcule_grade_from_reviews(reviews: list['Review']) -> 'Grade':
        if len(reviews) == 0:
            return Grade(0)
        return Grade(sum([review.grade.grade for review in reviews]) / len(reviews))


class Review(db.Model):

    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    review_grade = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __str__(self):
        return f"{self.author_name}: {self.content} ({self.grade})"

    def __repr__(self):
        return "<Review {}>" % self.id

    def to_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def commit(self) -> int:
        db.session.add(self)
        db.session.commit()
        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True

    @property
    def author_name(self) -> str:
        return User.get_user_name_by_id(self.author_id)

    @property
    def grade(self) -> Grade:
        return Grade(self.review_grade)

    @classmethod
    def get_all_reviews(cls) -> list['Review']:
        return cls.query.all()

    @classmethod
    def get_review_by_id(cls, review_id: int) -> 'Review':
        return cls.query.get(review_id)

    @classmethod
    def get_reviews_by_product_id(cls, product_id: int) -> list['Review']:
        return cls.query.filter_by(product_id=product_id).all()
