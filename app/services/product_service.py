from typing import Literal

import requests
from bs4 import BeautifulSoup

from app.models.product import Product
from app.services.provider_service import ProviderService
from app.utils.parse_int import parse_int


class ProductService:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    @staticmethod
    def get_all_products(query: str) -> list[Product]:
        products = ProductService.scrape_for_products(query)
        return products

    @staticmethod
    def get_product_list(
        product_markup: BeautifulSoup, tag: str, options: object
    ) -> list[BeautifulSoup]:
        products: list[BeautifulSoup] = product_markup.find_all(tag, options)
        return products

    @staticmethod
    def create_product(
        product_markup: BeautifulSoup,
        provider_name: Literal["XXL", "unkown"] = "unkown",
    ) -> Product:
        brand_span = product_markup.find("span", {"data-testid": "new-product-brand"})
        name_span = brand_span.find_next_sibling("span")

        product = Product(
            name=name_span.text,
            price=parse_int(
                product_markup.find("span", {"data-testid": "current-price"}).text
            ),
            brand=brand_span.text,
            provider=provider_name,
        )
        return product

    @staticmethod
    def scrape_for_products(search_query: str) -> list[Product]:
        providers = ProviderService.get_all_providers()

        for provider in providers:
            response = requests.get(
                provider.get_url(search_query), headers=ProductService.HEADERS
            )

            if response.status_code == 200:
                html = BeautifulSoup(response.text, "html.parser")

                product_list = ProductService.get_product_list(
                    html, "div", {"data-testid": "list-product"}
                )

                products: list[Product] = []
                for product in product_list:
                    products.append(
                        ProductService.create_product(product, provider.name)
                    )

                return products

            else:
                print(
                    "Failed to retrieve the page. Status code:",
                    response.status_code,
                )

        return []
