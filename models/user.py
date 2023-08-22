from models.base import BaseModel
from flask_login import UserMixin
from utils.database import db


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    cart = db.Column(db.JSON, nullable=False, default=[])
    # todo : add address and status (active, inactive, banned, etc)

    def get_id(self):
        return str(self.id)

    def add_item_to_cart(self, product, quantity=1):
        exists = any(item["id"] == product.id for item in self.cart)
        if exists:
            for item in self.cart:
                if item["id"] == product.id:
                    item["quantity"] += quantity
        else:
            self.cart.append({"id": product.id, "quantity": quantity})

    @property
    def cart_length(self):
        return len(self.cart)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

