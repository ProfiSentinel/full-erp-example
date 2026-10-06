from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

app = FastAPI(
    title="Modular ERP System API",
    description="REST API for managing storage, orders and partners",
    version="1.0.0"
)

@app.get("/",tags=["Health Check"])
def read_root():
    return {"status":"ok","message":"ERP backend is running"}


# --- PRODUCTS ENDPOINTS --- 
@app.get("/api/products", response_model=List[schemas.ProductResponse], tags=["Products"])
def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all products from database/catalog"""
    products =db.query(models.Product).offset(skip).limit(limit).all()
    return products

@app.get("/api/product/{product_id}", response_model=schemas.ProductResponse, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Detail of one product - ID product"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produkt nebyl nalezen.")
    return product



@app.post("/api/products", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Create new product"""
    # Check duplicity
    db_product = db.query(models.Product).filter(models.Product.sku == product.sku).first()
    if db_product:
        raise HTTPException(
            status_code= 400,
            detail = f"Product s kódem SKU '{product.sku}' již existuje."
        )

    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
