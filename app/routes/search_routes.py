from fastapi import APIRouter, HTTPException

from app.models.product import Product
from app.services.product_service import ProductService

router = APIRouter()


@router.get("/search/", response_model=list[Product])
def get_products(query: str) -> list[Product]:
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")

    return ProductService.get_all_products(query)
