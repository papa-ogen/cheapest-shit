from bs4 import BeautifulSoup

from app.models.product import Product
from app.models.provider import Provider
from app.services.product_service import ProductService
from app.utils.parse_int import parse_int

from .__mocks__.product_test_data_xxl import product_test_data


def test_get_products() -> None:
    html = BeautifulSoup(product_test_data, "html.parser")

    provider = Provider(
        name="XXL",
        provider_host="https://www.xxl.se",
        query="/search?query={search_query}",
        params={"sort": "PRICE_ASCENDING"},
        scrape_params={"data-testid": "list-product"},
        product_scrape_params=lambda product_markup: {
            "name": product_markup.find("span", {"data-testid": "new-product-brand"})
            .find_next_sibling("span")
            .text,
            "price": product_markup.find("span", {"data-testid": "current-price"}).text,
            "brand": product_markup.find(
                "span", {"data-testid": "new-product-brand"}
            ).text,
        },
    )

    product_list = ProductService.get_product_list(html, "div", provider.scrape_params)
    assert len(product_list) == 36

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

    assert products[0].name == "Hockey Laces Waxed Laces 1 Pair 23/24"
    assert products[0].price == 39.0
    assert products[0].brand == "Mohawke"
    assert products[0].provider == "XXL"
