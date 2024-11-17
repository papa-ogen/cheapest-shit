from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.config import init_db
from app.models.product import ProductResponseModel
from app.models.responses import ProductListResponse
from app.services.openapi_service import OpenApiService
from app.services.product_service import ProductService

router = APIRouter(dependencies=[Depends(init_db)])


# Will scrape for products and add them to the database
@router.get("/v1/search", response_model=ProductListResponse)
async def get_products1(query: str) -> ProductListResponse:
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")

    products = await ProductService.init(query)
    product_response = [
        ProductResponseModel.from_orm_with_vector(product) for product in products
    ]
    return ProductListResponse(
        total_amount_of_products=len(products), products=product_response
    )


# Only looks for existing products in the database
@router.get("/v2/search", response_model=ProductListResponse)
async def get_products2(query: str, limit: Optional[int] = None) -> ProductListResponse:
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    openapi_service = OpenApiService()
    query_vector = openapi_service.generate_product_vector(query)

    products = await ProductService.get_similar_products(query_vector, limit)

    sorted_products = sorted(
        products,
        key=lambda product: (
            product.price if product.price is not None else float("inf")
        ),
    )

    product_response = [
        ProductResponseModel.from_orm_with_vector(product)
        for product in sorted_products
    ]

    return ProductListResponse(
        total_amount_of_products=len(products), products=product_response
    )
