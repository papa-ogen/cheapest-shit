from bs4 import BeautifulSoup
from app.services.scrape import get_product_list
from .product_test_data_xxl import product_test_data

def test_get_products():
    html = BeautifulSoup(product_test_data, 'html.parser')

    products = get_product_list(html, 'div', {'data-testid': 'list-product'})
    assert len(products) == 36