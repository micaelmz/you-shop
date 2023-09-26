from models.base import BaseModel
from flask_login import UserMixin
from utils.database import db


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    cart = db.relationship('Cart', backref='user', order_by='Cart.id')

    def confirm(self):
        self.status = 1
        self.commit()

    def ban(self):
        self.status = 2
        self.commit()

    @property
    def is_active(self):
        return self.status == 1

    @property
    def is_banned(self):
        return self.status == 2

    @property
    def status_label(self):
        if self.is_active:
            return 'Ativo'
        elif self.is_banned:
            return 'Banido'
        return 'Inativo'

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
