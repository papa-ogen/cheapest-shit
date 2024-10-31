from unittest.mock import Mock

import pytest
from bs4 import BeautifulSoup

# from app.services.provider_service import ProviderService
from app.tests.__mocks__ import product_test_data_xxl

# from app.models.product import Product
# from app.services.product_service import ProductService


@pytest.fixture
def mock_provider() -> Mock:
    return Mock(
        name="XXL",
        provider_host="https://www.xxl.se",
        query="/search?query={search_query}",
        params={"sort": "PRICE_ASCENDING"},
        get_url=Mock(
            return_value="https://www.xxl.se/search?query=skridskor&sort=PRICE_ASCENDING"
        ),
    )


@pytest.fixture
def mock_product_markup() -> BeautifulSoup:
    # Mocked BeautifulSoup object structure for a product
    html = product_test_data_xxl
    return BeautifulSoup(html, "html.parser")


# @patch("app.services.product_service.requests.get")
# @patch("app.services.provider_service.ProviderService.get_all_providers")
# def test_get_all_products(
#     mock_get_all_providers: Mock, mock_requests_get: Mock, mock_provider, mock_product_markup
# ) -> None:
#     # Mocking ProviderService to return a list of providers
#     mock_get_all_providers.return_value = [mock_provider]

#     # Mocking the response of requests.get
#     mock_response = Mock()
#     mock_response.status_code = 200
#     mock_response.text = str(mock_product_markup)
#     mock_requests_get.return_value = mock_response

#     # Call the method
#     # product_list = ProductService.get_product_list(html, 'div', {'data-testid': 'list-product'})
#     products = ProductService.get_all_products("skridskor")

#     # Assert we got a list with the correct Product
#     assert isinstance(products, list)
#     assert len(products) == 1

#     # Validate product data
#     product = products[0]
#     assert isinstance(product, Product)
#     assert product.name == "Product Name"
#     assert product.price == 399
#     assert product.brand == "BrandName"
#     assert product.provider == "XXL"


# @patch("app.services.product_service.ProductService.get_product_list")
# def test_create_product(mock_get_product_list, mock_product_markup, mock_provider):
#     # Mock product list to return the mocked markup
#     mock_get_product_list.return_value = [mock_product_markup]

#     # Call create_product directly to check it processes correctly
#     product = ProductService.create_product(mock_product_markup, "XXL")

#     # Assert that create_product processed the product details
#     assert product.name == "Product Name"
#     assert product.price == 399
#     assert product.brand == "BrandName"
#     assert product.provider == "XXL"
