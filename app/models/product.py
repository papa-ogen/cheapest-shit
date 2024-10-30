from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Sample Product",
                "price": 19.99,
                "description": "A great product description!"
            }
        }