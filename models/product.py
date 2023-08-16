from models.review import Rating
from models.base import BaseModel
from utils.database import db


class Price:
    def __init__(self, new: float, old: float):
        self.new = new
        self.old = old

    @property
    def discount(self) -> float:
        return self.old - self.new

    def __str__(self):
        return self.label_price(self.new)

    @staticmethod
    def label_price(price: float) -> str:
        return "{:.2f}".format(price).replace('.', ',')


class Product(BaseModel):

    __tablename__ = 'product'
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price_current = db.Column(db.Float, nullable=False)
    price_old = db.Column(db.Float, nullable=False, default=0)
    on_sale = db.Column(db.Boolean, nullable=False, default=False)
    image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    additional_info = db.Column(db.JSON, nullable=True)
    additional_images = db.Column(db.JSON, nullable=True)
    reviews = db.relationship('Review', backref='product')

    @property
    def rating(self) -> Rating:
        return Rating.calculate_rating_from_reviews(self.reviews)

    @property
    def price(self) -> Price:
        return Price(self.price_current, self.price_old)

    @staticmethod
    def detect_color(img_url: str) -> str:
        dominant_color = 'Neutro'
        return dominant_color

    @classmethod
    def get_on_sale_products(cls) -> list['Product']:
        return cls.query.filter_by(on_sale=True).all()

    @classmethod
    def get_products_by_category_id(cls, category_id: int) -> list['Product']:
        return cls.query.filter_by(category_id=category_id).all()

    @classmethod
    def search_products_by_string(cls, search_string: str) -> list['Product']:
        return cls.query.filter(cls.name.contains(search_string) | cls.description.contains(search_string)).all()
