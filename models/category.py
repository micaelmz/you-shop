from database import db


class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Category {}>" % self.id

    def commit(self):
        db.session.add(self)
        db.session.commit()
        return self.id

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

