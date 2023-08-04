class Category:
    def __init__(self, id: int, name: str, image_url: str):
        self.id = id
        self.name = name
        self.image_url = image_url

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories(db):
        try:
            db.cursor.execute('SELECT * FROM category')
            rows = db.cursor.fetchall()
            categories = []
            for row in rows:
                categories.append(Category(*row))
            return categories
        except Exception as e:
            raise e

    @staticmethod
    def get_category_by_id(db, category_id: int):
        try:
            db.cursor.execute('SELECT * FROM category WHERE id = ?', (category_id,))
            row = db.cursor.fetchone()
            return Category(*row)
        except Exception as e:
            raise e

