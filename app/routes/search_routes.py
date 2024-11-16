from fastapi import APIRouter, Depends, HTTPException

from app.config import init_db
from app.models.product import ProductResponseModel
from app.models.responses import ProductListResponse
from app.services.product_service import ProductService

router = APIRouter(dependencies=[Depends(init_db)])


@router.get("/search/v1", response_model=ProductListResponse)
async def get_products(query: str) -> ProductListResponse:
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")

    products = await ProductService.init(query)
    product_response = [
        ProductResponseModel.from_orm_with_vector(product) for product in products
    ]
    return ProductListResponse(
        total_amount_of_products=len(products), products=product_response
    )


# add a v2 route that fetch data form vector db
