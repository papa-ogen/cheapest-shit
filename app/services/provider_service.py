from app.models.provider import Provider


class ProviderService:
    @staticmethod
    def get_all_providers() -> list[Provider]:
        providers = [
            Provider(name='XXL', provider_host='https://www.xxl.se', query='/search?query={search_query}', params={'sort': 'PRICE_ASCENDING'}),
            
        ]
        return providers
     
