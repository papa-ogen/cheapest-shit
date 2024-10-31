from fastapi import APIRouter, HTTPException
from app.services.product_service import ProductService
from app.models.product import Product

router = APIRouter()

@router.get("/search/", response_model=list[Product])
def get_products(query: str = None) -> list[Product]:
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    return ProductService.get_all_products(query)


# # Provider
# sort_by = 'PRICE_ASCENDING'
# search_query = 'skridskor'
# provider_host = 'https://www.xxl.se'
# URL = f'{provider_host}/search?query={search_query}&sort={sort_by}'

# @app.get(f"{ROOT_PATH}/search/:{search_query}")
# def read_root() -> dict[str, str]:
#     return {"Hello": "World"}
