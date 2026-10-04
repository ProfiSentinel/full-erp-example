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
class PartnerBase(BaseModel):
    company_name: str
    ico: Optional[str] = None
    dic: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_customer: bool = True
    is_supplier: bool = False

class PartnerCreate(PartnerBase):
    pass

class PartnerResponse(PartnerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


    # --- STOCK MOVEMENT SCHEMAS --- 
class StockMovementCreate(BaseModel):
    product_id: int
    movement_type: MovementType
    quantity: int = Field(gt=0) # ammount must by greatger than 0
    note: Optional[str] = None

class StockMovementResponse(StockMovementCreate):
    id: int
    created_at: datetime
    created_by_user_id: int

    model_config = ConfigDict(from_attributes=True)


# --- ORDER SCHEMAS ---
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0) #ammount must by greather than 0

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    unit_price: float
    vat_rate: float

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    partner_id: int
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    order_number: str
    partner_id: int
    status: OrderStatus
    total_without_vat: float
    total_vat: float
    total_with_vat: float
    created_at: datetime
    created_by_user_id: int
    items: List[OrderItemResponse] = None

    model_config = ConfigDict(from_attributes=True)





