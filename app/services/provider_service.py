from app.models.provider import Provider


class ProviderService:
    @staticmethod
    def get_all_providers() -> list[Provider]:
        providers = [
            Provider(
                name="XXL",
                provider_host="https://www.xxl.se",
                query="/search?query={search_query}",
                params={"sort": "PRICE_ASCENDING"},
                scrape_params={"data-testid": "list-product"},
                product_scrape_params=lambda product_markup: {
                    "name": product_markup.find(
                        "span", {"data-testid": "new-product-brand"}
                    )
                    .find_next_sibling("span")
                    .text,
                    "price": product_markup.find(
                        "span", {"data-testid": "current-price"}
                    ).text,
                    "brand": product_markup.find(
                        "span", {"data-testid": "new-product-brand"}
                    ).text,
                },
            ),
            Provider(
                name="Intersport",
                provider_host="https://www.intersport.se",
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
            ),
        ]
        return providers
