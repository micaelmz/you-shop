from utils.database import db


class Category(db.Model):

    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(500), nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Category {}>" % self.id

    def to_dict(self: object) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def commit(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True

    @classmethod
    def get_all_categories(cls):
        return cls.query.all()

    @classmethod
    def get_category_by_id(cls, id: int):
        return cls.query.get(id)

    @classmethod
    def search_categories_by_name(cls, name: str):
        return cls.query.filter(cls.name.contains(name)).all()
