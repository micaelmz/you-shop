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

