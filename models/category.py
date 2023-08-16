from models.base import BaseModel
from utils.database import db


class Category(BaseModel):
    __tablename__ = 'category'
    name = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    products = db.relationship('Product', backref='category')
