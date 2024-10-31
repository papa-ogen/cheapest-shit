from pydantic import BaseModel

class Provider(BaseModel):
    name: str
    provider_host: str
    query: str
    params: dict[str, str] = {}

    def get_url(self, search_query: str) -> str:
        return f"{self.provider_host}{self.query.format(search_query=search_query, **self.params)}"

    class Config:
        schema_extra = {
            "example": {
                "name": "XXL",
                "provider_host": "https://www.xxl.se",
                "query": "/search?query={search_query}",
                "params": {"sort": "PRICE_ASCENDING"},
                "get_url": "https://www.xxl.se/search?query=skridskor&sort=PRICE_ASCENDING"
            }
        }



