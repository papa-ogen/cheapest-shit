from bs4 import BeautifulSoup

from app.models.product import Product
from app.services.product_service import ProductService
from app.services.provider_service import ProviderService
from app.types import ProviderName

from .__mocks__.product_test_data_intersport import product_test_data


def test_get_products() -> None:
    html = BeautifulSoup(product_test_data, "html.parser")

    providers = ProviderService.get_all_providers()

    intersport_provider = next(
        (
            provider
            for provider in providers
            if provider.name == ProviderName.INTERSPORT
        ),
        None,
    )

    if intersport_provider is None:
        raise ValueError("Provider not found")

    product_list = ProductService.get_product_markup_list(
        html, "div", intersport_provider.scrape_params
    )
    assert len(product_list) == 33

    products: list[Product] = ProductService.extract_products_from_markup(
        product_markup_list=product_list, provider=intersport_provider
    )

    assert products[0].name == "Nylon 10x20 cm lagningslapp"
    assert products[0].price == 59
    assert products[0].brand == "Blue Line by Kleiber"
    assert products[0].provider == ProviderName.INTERSPORT
    assert (
        products[0].image
        == "https://cdn.intersport.se/cdn-cgi/imagedelivery/wT8bUgvMzuJDRcaEDgl0aQ/prod/159175601000_10/w=1536,h=1536,quality=75,fit=pad,background=%23f8f9fa"
    )
    assert (
        products[0].url
        == "/utrustning/ovrigt/blue-line-by-kleiber-nylon-10x20-cm-lagningslapp/svart"
    )
