from bs4 import BeautifulSoup

from app.models.product import Product
from app.services.product_service import ProductService

from .__mocks__.product_test_data_xxl import product_test_data


def test_get_products() -> None:
    html = BeautifulSoup(product_test_data, "html.parser")

    product_list = ProductService.get_product_list(
        html, "div", {"data-testid": "list-product"}
    )
    assert len(product_list) == 36

    products: list[Product] = []

    for product in product_list:
        products.append(ProductService.create_product(product, "XXL"))

    assert products[0].name == "Hockey Laces Waxed Laces 1 Pair 23/24"
    assert products[0].price == 39.0
    assert products[0].brand == "Mohawke"
    assert products[0].provider == "XXL"
