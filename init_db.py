import traceback
import sys
from app.database import engine, SessionLocal, Base
from app import models

def init_database():
    print("Creating database tables in erp.db....")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # check if database contain data
        if db.query(models.User).first():
            print("Database already contains data. Incialization skipped.")
            return

        print("Inserting testing data (seeding)...")

        # Testing users
        admin_user = models.User(
            username="admin",
            email="admin@erp.cz",
            hashed_password="hashed_admin_password:123",
            role=models.UserRole.ADMIN,
            is_active=True
        )

        sales_user = models.User(
            username="obchodnik",
            email="obchodnik@erp.cz",
            hashed_password="hashed_sale_password_123",
            role=models.UserRole.SALES,
            is_active=True
        )

        db.add_all([admin_user,sales_user])
        db.commit()

        # Testing category products
        cat_electro = models.Category(name="Elektronika", description="Počítače, komponenty a příslušenství")
        cat_office = models.Category(name="Kancelářské potřeby", description="Papír, psací potřeby a nábytek")
        db.add_all([cat_electro, cat_office])
        db.commit()

        # Testing products
        prod1 = models.Product(
            sku="EL-001",
            name="Bezdrátová myš Logitech",
            description="Optická ergonomická myš",
            category_id=cat_electro.id,
            purchase_price=350.0,
            selling_price=590.0,
            vat_rate=21.0,
            current_stock = 15,
            min_stock_level=5
        )

        prod2 = models.Product(
            sku="EL-002",
            name="27\" DELL Monitor",
            description="IPS QHD monitor",
            category_id=cat_electro.id,
            purchase_price=4200.0,
            selling_price=6490.0,
            vat_rate=21.0,
            current_stock=4, # above minimal requiements for testing
            min_stock_level=5
        )

        prod3 = models.Product(
            sku="KC-001",
            name="Kancelářský papír bílý (500ks)",
            description="Bílý papír 80g",
            category_id=cat_office.id,
            purchase_price=85.0,
            selling_price=139.0,
            vat_rate=21.0,
            current_stock=50,
            min_stock_level=10
        )
        db.add_all([prod1,prod2,prod3])
        db.commit()

        # Testing partner
        partner1 = models.Partner(
            company_name="ACME Solutions s.r.o.",
            ico="123456789",
            dic="CZ12345678",
            email="info@acme.cz",
            phone="+420 111 222 333",
            is_customer=True,
            is_supplier=False
        )

        db.add(partner1)
        db.commit()

        print("Database Succesfully iniciated and testing data ineserted.")

    except Exception as e:
        print(f"Error initializing database: {e}")
        traceback.print_exc() # pro výpis traceback do konzole při chybě (pouze pro testování)
        db.rollback()

    finally:
        db.close()

if __name__ == "__main__":
    init_database()

