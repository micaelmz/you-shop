from models.base import BaseModel
from utils.database import db


class User(BaseModel):
    __tablename__ = 'user'
    name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    cart = db.Column(db.JSON, nullable=False, default=[])

    def is_authenticated(self):
        pass

    def is_active(self):
        pass

    def is_anonymous(self):
        pass

    def get_id(self):
        return str(self.id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
