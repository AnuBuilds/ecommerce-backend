from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock_qty = Column(Integer, default=0)
    image_url = Column(String)
    category = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())