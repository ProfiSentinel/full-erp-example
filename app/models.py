from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum as SqlEnum, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

# -- ENUMS --
class UserRole(str, Enum): 
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    SALES = "SALES"
    WAREHOUSE = "WAREHOUSE"

class OrderStatus(str, Enum):
    DRAFT = "DRAFT"             # návrh objednávky
    CONFIRMED = "CONFIRMED"     # potvrzeno (blokuje sklad)
    DISPATCHED = "DISPATCHED"   # vyskladněno
    INVOICED = "INVOICED"       # fakturováno
    PAID = "PAID"               # zaplaceno
    CANCELLED = "CANCELLED"     # zrušeno   

class MovementType(str, Enum):
    IN = "IN"           # příjem na sklad
    OUT = "OUT"         # výdej ze skladu
    ADJU = "ADJUSTMENT" # inventurní korekce


# -- MODELS --
class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True,nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SqlEnum(UserRole), nullable=False, default=UserRole.SALES)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    #relationships
    orders = relationship("Order", back_populates="created_by_user")
    stock_movements = relationship("StockMovement", back_populates="created_by_user")

class Category(Base):
    """Product category model"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=True)

    #relationships
    products = relationship("Product", back_populates="category")


class Product(Base):
    """Product model"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True) #code product
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    purchase_price = Column(Integer, nullable=False) # purchase price without VAT 
    selling_price = Column(Integer, nullable=False) #selling price without VAT
    vat_rate = Column(Integer, nullable=False) # VAT rate in percentage

    current_stock = Column(Integer, nullable=False, default=0)
    min_stock_level = Column(Integer, nullable=False, default=5)

    #relationships
    category = relationship("Category", back_populates="products")
    stock_movements = relationship("StockMovement", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class Partner(Base):
    """Customers and Suppliers"""
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), nullable=False, index=True)
    ico = Column(String(20), unique=True, nullable=False, index=True)
    dic = Column(String(20), unique=True, nullable=True, index=True)
    email = Column(String(100), unique=True, nullable=True, index=True)
    phone = Column(String(20), nullable=True, index=True)

    is_customer = Column(Boolean, default=True)
    is_supplier = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    #relationships
    orders = relationship("Order", back_populates="partner")

class StockMovement(Base):
    """Stock movement model"""
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    movement_type = Column(SqlEnum(MovementType), nullable=False)
    quantity = Column(Integer, nullable=False)
    note= Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    #relationships
    product = relationship("Product", back_populates="stock_movements")
    created_by_user= relationship("User", back_populates="stock_movements")

class Order(Base):
    """Header of the order"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number= Column(String(50), unique=True, nullable=False, index=True)
    partner_id =Column(Integer,ForeignKey("partners.id"), nullable=False)
    status = Column(SqlEnum(OrderStatus), nullable=False, default=OrderStatus.DRAFT)

    total_without_vat = Column(Float, nullable=False, default=0.0)
    total_vat = Column(Float, nullable=False, default=0.0)
    total_with_vat = Column(Float, nullable=False, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    #relationships
    partner = relationship("Partner", back_populates="orders")
    created_by_user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    """Items of the order"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    quantity= Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False,)
    vat_rate= Column(Integer, nullable=False)

    #relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product",back_populates="order_items")