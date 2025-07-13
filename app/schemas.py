from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, Field

# -------------------------
# User Schemas
# -------------------------

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True

# -------------------------
# Product Schemas
# -------------------------

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    stock: Optional[int] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True

# -------------------------
# Cart Schemas
# -------------------------

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    product_name: Optional[str] = None  # Optional for convenience

    class Config:
        orm_mode = True

# -------------------------
# Order Schemas
# -------------------------

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: OrderStatus
    created_at: datetime

    class Config:
        orm_mode = True

class Order(OrderBase):
    items: List[OrderItemOut]  # ✅ updated from cart_items → items

    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
