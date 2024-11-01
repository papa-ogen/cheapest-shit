from fastapi import APIRouter, HTTPException

from app.models.responses import ProductListResponse
from app.services.product_service import ProductService

router = APIRouter()


@router.get("/search/", response_model=ProductListResponse)
def get_products(query: str) -> ProductListResponse:
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")

    products = ProductService.scrape_for_products(query)
    return ProductListResponse(
        total_amount_of_products=len(products), products=products
    )
