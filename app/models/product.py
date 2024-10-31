from pydantic import BaseModel
from typing import Optional, Literal

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    brand: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None
    provider: Literal["xxl", "unkown"] = "unkown"

    class Config:
        schema_extra = {
            "example": {
                "name": "Sample Product",
                "price": 19.99,
                "description": "A great product description!"
            }
        }