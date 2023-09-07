from models.base import BaseModel
from utils.database import db


class Cart(BaseModel):
    __tablename__ = 'cart'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    product = db.relationship('Product', backref='cart')

    def __add__(self, qnt):
        self.quantity += qnt
        self.commit()
        return self.quantity

    def __sub__(self, qnt):
        self.quantity -= qnt
        return self.quantity

    def update_item(self, quantity):
        self.quantity = quantity
        self.commit()
        return True

    def delete_item(self):
        self.delete()
        return True

    def __len__(self):
        return self.quantity

    @classmethod
    def get_or_create_cart(cls, user_id, product_id):
        cart = cls.query.filter_by(user_id=user_id, product_id=product_id).first()
        if not cart:
            cart = Cart(user_id=user_id, product_id=product_id)
            cls.commit(cart)
        return cart
