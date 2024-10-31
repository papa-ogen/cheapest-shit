from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    name: str
    price: Optional[int] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None
    provider: Literal["XXL", "unkown"] = "unkown"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Sample Product",
                "price": 19.99,
                "description": "A great product description!",
            }
        }
    )
