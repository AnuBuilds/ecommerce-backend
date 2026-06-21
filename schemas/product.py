from pydantic import BaseModel
from typing import Optional

# Used when Admin CREATES a product
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_qty: int
    image_url: Optional[str] = None
    category: Optional[str] = None

# Used when Admin UPDATES a product (all fields optional)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_qty: Optional[int] = None
    image_url: Optional[str] = None
    category: Optional[str] = None

# What we RETURN to the frontend
class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock_qty: int
    image_url: Optional[str]
    category: Optional[str]

    class Config:
        from_attributes = True