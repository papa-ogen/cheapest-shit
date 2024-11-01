from typing import Any, Callable, Dict

from pydantic import BaseModel, ConfigDict

from app.types import ProviderName


class Provider(BaseModel):
    name: ProviderName
    provider_host: str
    query: str
    params: dict[str, str] = {}
    scrape_params: dict[str, str] = {}
    product_scrape_params: Callable[[Any], Dict[str, Any]]

    def get_url(self, search_query: str) -> str:
        return f"{self.provider_host}{self.query.format(search_query=search_query, **self.params)}"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "XXL",
                "provider_host": "https://www.xxl.se",
                "query": "/search?query={search_query}",
                "params": {"sort": "PRICE_ASCENDING"},
                "scrape_params": {"data-testid": "list-product"},
                "product_scrape_params": {
                    "name": "product_markup.find('span', {'data-testid': 'new-product-brand'}).find_next_sibling('span').text",
                    "price": "product_markup.find('span', {'data-testid': 'current-price'}).text",
                    "brand": "product_markup.find('span', {'data-testid': 'new-product-brand'}).text",
                    "image": "product_markup.find('img', {'data-nimg': 1})['src']",
                    "url": "product_markup.find('a')['href']",
                },
                "get_url": "https://www.xxl.se/search?query=skridskor&sort=PRICE_ASCENDING",
            }
        }
    )
