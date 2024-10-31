import requests
from app.models.product import Product
from bs4 import BeautifulSoup

from app.utils.parse_int import parse_int

class ProductService:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    @staticmethod
    def get_all_products(query: str) -> list[Product]:
        products = ProductService.scrape_xxl(query)
        return products

    @staticmethod
    def get_product_list(product_markup: BeautifulSoup, tag: str, options: object) -> list[BeautifulSoup]:
        products = product_markup.find_all(tag, options)
        return products

    @staticmethod
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
    
    @staticmethod
    def scrape_xxl(search_query: str) -> list[Product]:
        # Provider
        sort_by = 'PRICE_ASCENDING'
        provider_host = 'https://www.xxl.se'
        url = f'{provider_host}/search?query={search_query}&sort={sort_by}'

        response = requests.get(url, headers=ProductService.HEADERS)

        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'html.parser')

            product_list = ProductService.get_product_list(html, 'div', {'data-testid': 'list-product'})

            products: list[Product] = []
            for product in product_list:
                print(product)
                products.append(ProductService.create_product(product))

            return products
                
        else:
            print("Failed to retrieve the page. Status code:", response.status_code)