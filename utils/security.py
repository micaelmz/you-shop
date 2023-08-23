import datetime
import requests
import os

SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')


def calculate_salting_length():
    current_year = datetime.datetime.now().year

    return int((current_year - 2000) * 0.3)


def validate_recaptcha(secret_response):
    verify_response = requests.post(
        url=f'https://www.google.com/recaptcha/api/siteverify?secret={SECRET_KEY}&response={secret_response}').json()
    return verify_response['success']


if __name__ == '__main__':
    salting_length = calculate_salting_length()
    print(f"Comprimento de salting sugerido: {salting_length}")
