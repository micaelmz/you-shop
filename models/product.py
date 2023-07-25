from colorthief import ColorThief
import requests
import datetime


class Grade:
    def __init__(self, grade):
        self.grade = grade
        self.integer = int(grade)
        self.decimal = int(round((grade - self.integer) * 10))

    def __str__(self):
        return f"{self.integer},{self.decimal}"


class Price:
    def __init__(self, new, old):
        self.new = new
        self.old = old

    def __str__(self):
        return self.format_price(self.new)

    def format_price(self, price):
        return "{:.2f}".format(price)


class Review:
    def __init__(self, id, author, content, grade):
        self.id = id
        self.author = author
        self.content = content
        self.grade = Grade(grade)
        self.date = datetime.datetime.now().strftime('%d-%m-%Y')

    def __str__(self):
        return f"{self.author}: {self.content}"


class Product:
    def __init__(self, id, name, price, category, image_url, description, reviews: list, grade=0, price_old=0):
        self.id = id
        self.name = name
        self.price = Price(price, price_old)
        self.category = category
        self.image_thumb = image_url
        self.extra_images = []
        self.description = description
        self.reviews = reviews
        self.grade = self.calculate_grade(self.reviews)
        self.color = self.detect_color()
        # self.image = f"img/{category.name.lower()}/{name.lower()}.jpg"

    def __str__(self):
        return f"{self.name} - {self.price}"

    def detect_color(self) -> str:
        raw_img = requests.get(self.image_thumb, stream=True).raw
        color_thief = ColorThief(raw_img)
        dominant_color = color_thief.get_color(quality=1)
        return dominant_color

    def calculate_grade(self, reviews: list) -> Grade:
        if len(reviews) == 0:
            return Grade(0)
        grades = [review.grade.grade for review in reviews]
        return Grade(sum(grades) / len(grades))
