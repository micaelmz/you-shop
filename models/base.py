from utils.database import db


class BaseModel(db.Model):
    """
    Base model for all models in the application. Provides basic CRUD functionality and common methods
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    def commit(self) -> int:
        """
        Commit the object to the database
        :return: The generated id of the object
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self, **kwargs) -> 'BaseModel':
        """
        Update the object based on the properties passed in through kwargs
        :param kwargs:
        :return: The updated object
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self) -> bool:
        """
        Delete the object from the database
        :return: True if the object was deleted, False otherwise
        :raises IntegrityError: if the object cannot be deleted due to foreign key constraints
        """
        db.session.delete(self)
        db.session.commit()
        return True

    def to_dict(self: object) -> dict:
        """
        Convert the object to a dictionary
        :return: A dictionary representation of the object
        """
        base_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if hasattr(self, 'date'):
            base_dict['date'] = self.date.strftime('%Y-%m-%d %H:%M:%S')
        return base_dict

    def to_dict_with_selected_properties(self: object, selected_properties: list) -> dict:
        """
        Convert the object to a dictionary, including specified properties defined using the @property decorator
        :param selected_properties: List of property names to include in the dictionary
        :return: A dictionary representation of the object with selected properties
        """
        base_dict = self.to_dict()

        for prop_name in selected_properties:
            if hasattr(self, prop_name):
                # If the property is a Rating object, only include the rating value
                if prop_name == 'rating' and hasattr(getattr(self, prop_name), 'rating'):
                    base_dict[prop_name] = getattr(self, prop_name).rating
                else:
                    base_dict[prop_name] = getattr(self, prop_name)

        return base_dict

    @classmethod
    def get_all(cls) -> list['BaseModel']:
        """
        Get all objects of this type from the database
        :return: A list of all objects of this type
        :raises NoResultFound: if no objects of this type exist in the database
        """
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id: int) -> 'BaseModel':
        """
        Get an object of this type from the database by its id
        :param id:
        :return The object with the given id
        :raises NoResultFound: if no object with the given id exists in the database
        """
        return cls.query.get(id)

    @classmethod
    def search_by_name(cls, name: str) -> list['BaseModel']:
        """
        Search for objects of this type in the database by their name
        :param name:
        :return: A list of objects with the given name
        :raises AttributeError: if the attribute name does not exist for this type of object
        """
        return cls.query.filter(cls.name.contains(name)).all()
