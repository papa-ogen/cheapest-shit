from bs4 import BeautifulSoup

from app.models.product import Product
from app.services.product_service import ProductService
from app.services.provider_service import ProviderService
from app.types import ProviderName

from .__mocks__.product_test_data_xxl import product_test_data


def test_get_products() -> None:
    html = BeautifulSoup(product_test_data, "html.parser")

    providers = ProviderService.get_all_providers()

    xxl_provider = next((provider for provider in providers if ProviderName.XXL), None)

    if xxl_provider is None:
        raise ValueError("Provider not found")

    product_list = ProductService.get_product_markup_list(
        html, "div", xxl_provider.scrape_params
    )
    assert len(product_list) == 36

    products: list[Product] = ProductService.extract_products_from_markup(
        product_markup_list=product_list, provider=xxl_provider
    )

    assert products[0].name == "Hockey Laces Waxed Laces 1 Pair 23/24"
    assert products[0].price == 39.0
    assert products[0].brand == "Mohawke"
    assert products[0].provider == ProviderName.XXL
    assert (
        products[0].image
        == "https://www.xxl.se/filespin/04dd9796dd284abc920e1e14fff02884?quality=75&bgcolor=efefef&resize=640%2C640"
    )
    assert (
        products[0].url
        == "/mohawke-hockey-laces-waxed-laces-1-pair-23-24-svart/p/1118004_3_Style"
    )
