import datetime


def calculate_salting_length():
    current_year = datetime.datetime.now().year

    return int((current_year - 2000) * 0.3)


if __name__ == '__main__':
    salting_length = calculate_salting_length()
    print(f"Comprimento de salting sugerido: {salting_length}")
