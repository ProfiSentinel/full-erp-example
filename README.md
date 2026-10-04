# 🏢 Modular ERP System Core (v2)

A modern sales and inventory ERP system built with Python, FastAPI, and SQLAlchemy. This project is designed as a portfolio showcase of advanced software architecture, ORM mapping, Pydantic data validation, and automated testing.

## 🛠 Tech Stack
- **Backend:** Python 3.11+, FastAPI
- **ORM & Database:** SQLAlchemy, SQLite (ready for PostgreSQL)
- **Data Validation:** Pydantic v2
- **Frontend (Planned):** HTMX + Jinja2 + Tailwind CSS
- **Testing:** Pytest

## 📌 Development Progress
- [x] Architecture design and project structure
- [x] ORM models (Users, Products, Stock Movements, Orders, Partners)
- [x] Pydantic schemas (DTOs) for input/output validation
- [x] Database initialization & test data seeding script (`init_db.py`)
- [ ] REST API endpoints (CRUD)
- [ ] Web GUI via HTMX
- [ ] Pytest test suite

## 🚀 Database Setup & Running
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python init_db.py