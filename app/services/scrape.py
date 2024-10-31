import requests
from bs4 import BeautifulSoup

from app.models.product import Product

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

def parse_int(s: str) -> int:
    num_str = ''
    for char in s:
        if char.isdigit():  # Check if the character is a digit
            num_str += char  # Add it to the result string
        else:
            break  # Stop at the first invalid character
    return int(num_str) if num_str else None  # Convert to int or return None if empty


def get_product_list(product_markup: BeautifulSoup, tag: str, options: object) -> list[BeautifulSoup]:
    products = product_markup.find_all(tag, options)
    return products

def create_product(product_markup: BeautifulSoup) -> Product:
    brand_span = product_markup.find('span', {'data-testid': 'new-product-brand'})
    name_span = brand_span.find_next_sibling('span')

    product = Product(
        name=name_span.text,
        price=parse_int(product_markup.find('span', {'data-testid': 'current-price'}).text),
        brand=brand_span.text,
        provider='xxl'
    )
    return product

def scrape_xxl(search_query: str) -> list[Product]:
    # Provider
    sort_by = 'PRICE_ASCENDING'
    provider_host = 'https://www.xxl.se'
    url = f'{provider_host}/search?query={search_query}&sort={sort_by}'


    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html = BeautifulSoup(response.text, 'html.parser')

        product_list = get_product_list(html, 'div', {'data-testid': 'list-product'})

        products: list[Product] = []
        for product in product_list:
            products.append(create_product(product))

        return products
            
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)