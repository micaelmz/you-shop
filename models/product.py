class Product:
    def __init__(self, id, name, price, category):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.rating = 0
        self.image = f"img/{category.name.lower()}/{name.lower()}.jpg"

    def __str__(self):
        return f"{self.name} - {self.price}"
