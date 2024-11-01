from typing import List

from pydantic import BaseModel

from app.models.product import Product


class ProductListResponse(BaseModel):
    total_amount_of_products: int
    products: List[Product]
