from models.base import BaseModel
from flask_login import UserMixin
from utils.database import db


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    cart = db.relationship('Cart', backref='user')

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

