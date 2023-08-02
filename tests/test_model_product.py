import pytest
from models.product import Product, Price
from mock_data import test_products, test_reviews
from database import Database
import datetime

# todo: criar DDL para o mock do banco de dados, para que os testes não dependam do arquivo test_db.db
db = Database('../test_db.db')


def test_price_format_price():
    price = Price(25.99, 15.5)
    assert price.format_price(25.99) == "25,99"
    assert price.format_price(15.5) == "15,50"


def test_price_str():
    price = Price(29.95, 20.0)
    assert str(price) == "29,95"


def test_product_detect_color():
    pass


def test_commit_product():
    first = Product.commit_product(db, test_products[0])
    assert first == 1
    second = Product.commit_product(db, test_products[1])
    assert second == 2


def test_get_all_product():
    products = Product.get_all_products(db)
    assert len(products) != 0
    assert len(products) == len(test_products)

    for i in range(len(products)):
        assert str(products[i]) == str(test_products[i])


def test_get_product_by_id():
    product = Product.get_product_by_id(db, 1)
    assert str(product) == str(test_products[0])


def test_db_handle():
    with pytest.raises(Exception) as e:
        Product.get_product_by_id(db, 999)  # 999 is an invalid id
    assert "Erro na função 'Get Product By Id' do banco de dados: " in str(e.value)


def test_more_information_json():
    pass
