from database import db


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    cart = db.Column(db.JSON, nullable=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<User {}>" % self.id

    def commit(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True

    @classmethod
    def get_all_users(cls) -> list['User']:
        return cls.query.all()

    @classmethod
    def get_user_by_id(cls, user_id: int) -> 'User':
        return cls.query.get(user_id)

    @classmethod
    def get_user_name_by_id(cls, user_id: int) -> str:
        return cls.query.get(user_id).name
