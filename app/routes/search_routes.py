from typing import Literal

from fastapi import APIRouter, HTTPException

from app.models.responses import ProductListResponse
from app.services.product_service import ProductService

router = APIRouter()


@router.get("/search/", response_model=ProductListResponse)
def get_products(
    query: str, order_by: Literal["asc", "desc"] = "asc"
) -> ProductListResponse:
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")

    products = ProductService.scrape_for_products(query)

    sorted_products = sorted(
        products,
        key=lambda product: product.price
        if product.price is not None
        else float("inf"),
        reverse=(order_by == "desc"),
    )

    return ProductListResponse(
        total_amount_of_products=len(products), products=sorted_products
    )
