from models.base import BaseModel
from utils.database import db
from models.user import User
from datetime import datetime


class Rating:
    def __init__(self, rating: float):
        self.rating = rating
        self.integer = int(rating)
        self.decimal = int(round((rating - self.integer) * 10))

    def __str__(self):
        return f"{self.integer},{self.decimal}"

    @staticmethod
    def calculate_rating_from_reviews(reviews: list['Review']) -> 'Rating':
        if len(reviews) == 0:
            return Rating(0)
        return Rating(sum([review.rating.rating for review in reviews]) / len(reviews))


class Review(BaseModel):
    __tablename__ = 'review'
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    review_rating = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __str__(self):
        return f"{self.author_name}: {self.content} ({self.rating})"

    @property
    def author_name(self) -> str:
        return User.get_user_name_by_id(self.author_id)

    @property
    def rating(self) -> Rating:
        return Rating(self.review_rating)

    @classmethod
    def get_reviews_by_author_id(cls, author_id: int) -> list['Review']:
        return cls.query.filter_by(author_id=author_id).all()

    @classmethod
    def get_reviews_by_product_id(cls, product_id: int) -> list['Review']:
        return cls.query.filter_by(product_id=product_id).all()
