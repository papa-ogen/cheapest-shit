from sqlite3 import IntegrityError

import numpy as np
import requests
from bs4 import BeautifulSoup

from app.models.product import Product
from app.models.provider import Provider
from app.models.query import Query
from app.services.openapi_service import OpenApiService
from app.services.provider_service import ProviderService
from app.utils.parse_int import parse_int


class ProductService:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    @staticmethod
    async def init(search_query: str) -> list[Product]:
        # search in db for query, if match get products from that query with qdrant
        # if query does not exist, add query to queries table and scrape for products

        existing_query = await Query.filter(query=search_query).first()

        if existing_query:
            print("Query already exist")
            # fetch products from db with vector DB to get relevant products
            products: list[Product] = await Product.filter(name=existing_query).all()
            return products

        print("Add Query to DB")
        await Query.create(query=search_query)

        products = ProductService.scrape_for_products(search_query)

        try:
            # Extract URLs of the products you want to insert
            product_urls = [product.url for product in products]

            existing_products = await Product.filter(url__in=product_urls).all()
            existing_urls = [product.url for product in existing_products]

            # Filter out the products that already exist (based on URL)
            new_products = [
                product for product in products if product.url not in existing_urls
            ]

            openapi_service = OpenApiService()

            for product in new_products:
                vector = openapi_service.generate_product_vector(
                    f"{product.name} {product.description} {product.url}"
                )
                product.vector = vector

            for product in new_products:
                if isinstance(product.vector, np.ndarray):
                    product.vector = product.vector.tolist()

            if new_products:
                print(f"Bulk create products {len(new_products)}")

                await Product.bulk_create(new_products)
            else:
                print("No new products to add.")
        except IntegrityError as e:
            print(f"Error occurred while adding products: {e}")

        # TODO: search for products in vector DB, products now return from scrape instead of DB
        return products

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
