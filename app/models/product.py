from typing import Optional

from pydantic import BaseModel
from tortoise import fields
from tortoise.models import Model

from app.types import ProviderName


class Product(Model):
    name = fields.CharField(max_length=255)
    price = fields.IntField(null=True)
    description = fields.TextField(null=True)
    brand = fields.CharField(max_length=255, null=True)
    url = fields.CharField(max_length=512, null=True)
    image = fields.CharField(max_length=512, null=True)
    provider = fields.CharEnumField(ProviderName)

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

    class Config:
        orm_mode = True  # This tells Pydantic to treat ORM models as dictionaries
        from_attributes = True  # Allows using from_orm()
