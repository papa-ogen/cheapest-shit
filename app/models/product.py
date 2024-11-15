from typing import Optional

import numpy as np
from pydantic import BaseModel, Field
from tortoise import fields
from tortoise.models import Model
from tortoise_vector.field import VectorField

from app.types import ProviderName


class Product(Model):
    name = fields.CharField(max_length=255)
    price = fields.IntField(null=True)
    description = fields.TextField(null=True)
    brand = fields.CharField(max_length=255, null=True)
    url = fields.CharField(max_length=512, null=True)
    image = fields.CharField(max_length=512, null=True)
    provider = fields.CharEnumField(ProviderName)
    vector = VectorField(vector_size=1536)

    class Meta:
        table = "products"

    # Optionally add a string representation for better readability
    def __str__(self) -> str:
        return f"Product(name={self.name}, provider={self.provider})"


class ProductResponseModel(BaseModel):
    name: str
    price: Optional[int] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None
    provider: ProviderName
    vector: list[float] = Field(
        ..., description="The embedding vector as a list of floats"
    )

    class Config:
        orm_mode = True  # This tells Pydantic to treat ORM models as dictionaries
        from_attributes = True  # Allows using from_orm()

    @classmethod
    def from_orm_with_vector(cls, product: Product) -> "ProductResponseModel":
        """
        Custom method to convert a Product ORM instance to a ProductResponseModel
        while serializing the vector to a list of floats.
        """
        vector_list = (
            product.vector.tolist() if isinstance(product.vector, np.ndarray) else []
        )
        return cls(
            name=product.name,
            price=product.price,
            description=product.description,
            brand=product.brand,
            url=product.url,
            image=product.image,
            provider=product.provider,
            vector=vector_list,
        )
