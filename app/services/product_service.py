import requests
from bs4 import BeautifulSoup

from app.models.product import Product
from app.models.provider import Provider
from app.services.provider_service import ProviderService
from app.utils.parse_int import parse_int


class ProductService:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    @staticmethod
    def get_product_markup_list(
        product_markup: BeautifulSoup, tag: str, options: object
    ) -> list[BeautifulSoup]:
        products: list[BeautifulSoup] = product_markup.find_all(tag, options)
        return products

    @staticmethod
    def extract_products_from_markup(
        product_markup_list: list[BeautifulSoup], provider: Provider
    ) -> list[Product]:
        products = []
        for product_markup in product_markup_list:
            scrape_params = provider.product_scrape_params(product_markup)
            products.append(
                Product(
                    name=scrape_params["name"],
                    price=parse_int(scrape_params["price"]),
                    brand=scrape_params["brand"],
                    provider=provider.name,
                    image=scrape_params.get("image"),
                    url=scrape_params.get("url"),
                )
            )
        return products

    @staticmethod
    def scrape_for_products(search_query: str) -> list[Product]:
        providers = ProviderService.get_all_providers()

        products: list[Product] = []

        for provider in providers:
            response = requests.get(
                provider.get_url(search_query), headers=ProductService.HEADERS
            )

            if response.status_code == 200:
                html = BeautifulSoup(response.text, "html.parser")

                # get products from markup
                product_markup_list = ProductService.get_product_markup_list(
                    html, "div", provider.scrape_params
                )

                # iterate over products and extract data
                products += ProductService.extract_products_from_markup(
                    product_markup_list, provider
                )

            else:
                print(
                    "Failed to retrieve the page. Status code:",
                    response.status_code,
                )

        # TODO: move to endpoint as query param
        sorted_products = sorted(
            products,
            key=lambda product: (
                product.price if product.price is not None else float("inf")
            ),
        )

        return sorted_products
