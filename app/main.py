from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

app = FastAPI(
    title="Modular ERP System API",
    description="REST API for managing storage, orders and partners",
    version="1.0.0"
)

# Configuration folder with templates
templates = Jinja2Templates(directory="app/templates")

# --- Frontends endpoints (HTML + HTMX) --- 
@app.get("/products-ui", response_class=HTMLResponse, include_in_schema=False)
def products_ui(request: Request, db: Session = Depends(get_db)):
    """Rendering the products overview page"""
    products = db.query(models.Product).all()
    categories = db.query(models.Category).all()
    return templates.TemplateResponse(
        request = request,
        name = "products.html",
        context = {"products": products, "categories": categories}
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


# POST endpoint for HTMX form
@app.post("/products-ui", response_class=HTMLResponse, include_in_schema=False)
def create_product_ui(
    request:Request,
    sku: str = Form(...),
    name: str = Form(...),
    category_id: int = Form(...),
    purchase_price: float = Form(...),
    selling_price: float = Form(...),
    vat_rate: float = Form(21.0),
    current_stock: int = Form(0),
    min_stock_level: int = Form(5),
    description: str | None = Form(None),
    db: Session = Depends(get_db)
):
    """HTMX form processing: creates a product and returns only its HTML row"""
    #check duplicity
    db_product = db.query(models.Product).filter(models.Product.sku == sku).first()
    if db_product:
        raise HTTPException(status_code=400, detail="SKU již existuje.")

    new_product = models.Product(
        sku = sku,
        name = name,
        description = description,
        category_id = category_id,
        purchase_price = purchase_price,
        selling_price = selling_price,
        vat_rate = vat_rate,
        current_stock = current_stock,
        min_stock_level = min_stock_level
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # We will return only a partial template (a single <tr> row)
    return templates.TemplateResponse(
        request = request,
        name = "partials/product_row.html",
        context = {"product": new_product}
    )