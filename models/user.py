from models.base import BaseModel
from utils.database import db


class User(BaseModel):
    __tablename__ = 'user'
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    cart = db.Column(db.JSON, nullable=True)

    @classmethod
    def get_user_name_by_id(cls, user_id: int) -> str:
        return cls.query.get(user_id).name
