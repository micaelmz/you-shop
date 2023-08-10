import json
from models.review import Review, Grade
from database import db
from sqlalchemy import event


class Price:
    def __init__(self, new: float, old: float):
        self.new = new
        self.old = old

    def __str__(self):
        return self.label_price(self.new)

    @staticmethod
    def label_price(price: float) -> str:
        return "{:.2f}".format(price).replace('.', ',')


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    price_current = db.Column(db.Float, nullable=False)
    price_old = db.Column(db.Float, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    promotion = db.Column(db.Boolean, nullable=False)
    image_thumb = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    additional_info = db.Column(db.JSON, nullable=True)
    extra_images = db.Column(db.JSON, nullable=True)
    reviews = Review.get_reviews_by_product_id(id)

    def __str__(self):
        return f"{self.name} - {self.price_current}"

    def __repr__(self):
        return "<Product {}>" % self.id

    def commit(self) -> int:
        db.session.add(self)
        db.session.commit()
        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True

    @staticmethod
    def detect_color(img_url: str) -> str:
        dominant_color = 'Neutro'
        return dominant_color

    @classmethod
    def get_all_products(cls) -> list['Product']:
        return cls.query.all()

    @classmethod
    def get_product_by_id(cls, product_id: int) -> 'Product':
        return cls.query.get(product_id)

    @classmethod
    def get_promotional_products(cls) -> list['Product']:
        return cls.query.filter_by(promotion=True).all()

    @classmethod
    def get_products_by_category_id(cls, category_id: int) -> list['Product']:
        return cls.query.filter_by(category=category_id).all()

    @classmethod
    # todo: test if it's insensitive
    def search_products_by_string(cls, search_string: str) -> list['Product']:
        return cls.query.filter(cls.name.contains(search_string) | cls.description.contains(search_string)).all()


@event.listens_for(Product, 'before_insert')
@event.listens_for(Product, 'load')
def initialize(product, *args, **kwargs):
    product.price = Price(product.price_current, product.price_old)
    product.reviews = Review.get_reviews_by_product_id(product.id)
    product.grade = Grade.calcule_grade_from_reviews(product.reviews)
