from bs4 import BeautifulSoup

from app.models.product import Product
from app.models.provider import Provider
from app.services.product_service import ProductService
from app.utils.parse_int import parse_int

from .__mocks__.product_test_data_intersport import product_test_data


def test_get_products() -> None:
    html = BeautifulSoup(product_test_data, "html.parser")

    provider = Provider(
        name="Intersport",
        provider_host="https://www.intersport.se/",
        query="/katalog?q={search_query}",
        params={"sort": "price%3Aascending"},
        scrape_params={"data-sentry-component": "ProductCard"},
        product_scrape_params=lambda product_markup: {
            "name": product_markup.find("a", {"class": "product-model"}).text,
            "price": product_markup.find(
                "span", {"data-sentry-component": "PriceTag"}
            ).text,
            "brand": product_markup.find("a", {"class": "product-brand"}).text,
        },
    )

    product_list = ProductService.get_product_list(html, "div", provider.scrape_params)
    assert len(product_list) == 33

    products: list[Product] = []
    for product in product_list:
        scrape_params = provider.product_scrape_params(product)

        products.append(
            Product(
                name=scrape_params["name"],
                price=parse_int(scrape_params["price"]),
                brand=scrape_params["brand"],
                provider=provider.name,
            )
        )

    assert products[0].name == "Nylon 10x20 cm lagningslapp"
    assert products[0].price == 59
    assert products[0].brand == "Blue Line by Kleiber"
    assert products[0].provider == "Intersport"
