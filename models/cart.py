from models.base import BaseModel
from utils.database import db


class Cart(BaseModel):
    __tablename__ = 'cart'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    product = db.relationship('Product', backref='cart')

    def __add__(self, other):
        self.quantity += other
        return self.quantity

    def __sub__(self, other):
        self.quantity -= other
        return self.quantity

    def delete_item(self):
        pass

    def __len__(self):
        return self.quantity
