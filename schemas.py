from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models import UserRole, OrderStatus, MovementType


# --- USER SCHEMAS ---
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.SALES
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# --- CATEGORY SCHEMAS ---
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- PRODUCT SCHEMAS ---
class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category_id: int
    purchase_price: float
    selling_price: float
    vat_rate: float = Field(default=21.0, ge=0.0)
    current_stock: int = Field(default=0, ge=0)
    min_stock_level: int = Field(default=5, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)


# --- PARTNER SCHEMAS ---
class PartnerBase



