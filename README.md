# Modulární ERP Systém

Lehký, rychlý a modulární ERP systém postavený na moderním Python backendu s reaktivním frontendem bez nutnosti složitých JavaScriptových frameworků.

## 🚀 Hlavní technologie (Tech Stack)

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3)
- **ORM / Databáze:** [SQLAlchemy](https://www.sqlalchemy.org/) + SQLite
- **Validace dat:** [Pydantic v2](https://docs.pydantic.dev/) (včetně `email-validator`)
- **Šablonovací systém:** [Jinja2](https://jinja.palletsprojects.com/)
- **Frontend & Styling:** [Tailwind CSS](https://tailwindcss.com/) (přes CDN) + [HTMX](https://htmx.org/)
- **Webový server:** [Uvicorn](https://www.uvicorn.org/)

---

## ⚙️ Dosavadní progress a plánované funkce

### Hotové funkcionality:
- [x] **REST API pro produkty:** Plně funkční backendové API dostupné na `/api/products`.
- [x] **Interaktivní API dokumentace:** Automaticky generované Swagger UI rozhraní na `/docs`.
- [x] **Databázové modely:** Návrh relací v SQLAlchemy (`Product`, `Category`) s podporou nákupních/prodejních cen a DPH.
- [x] **Uživatelské rozhraní (`/products-ui`):** Přehledná HTML stránka s katalogem produktů se stylováním v Tailwind CSS.
- [x] **Inicializační skript:** Automatické založení databázové struktury a vzorových dat (`init_db.py`).

### Plánovaný vývoj (Roadmap):
- [ ] **HTMX Formulář:** Reaktivní přidávání nových produktů do tabulky bez přenačtení stránky.
- [ ] **Správa produktů:** Možnost úpravy a mazání produktů přímo z UI v reálném čase.
- [ ] **Kategorie a sklady:** Modul pro správu kategorií produktů a sledování pohybů na skladě.
- [ ] **Autentizace:** Registrace, přihlašování a správa uživatelských rolí (např. admin vs. operátor).
- [ ] **Objednávky a fakturace:** Vytváření odběratelských objednávek a generování faktur.

---

## 📁 Struktura projektu

```text
full-erp-example/
├── app/
│   ├── static/              # Statické soubory (CSS, JS, obrázky)
│   ├── templates/           # Jinja2 HTML šablony
│   │   ├── base.html        # Hlavní layout aplikace
│   │   └── products.html    # Stránka katalogu produktů
│   ├── database.py          # Připojení k SQLite & SessionLocal
│   ├── main.py              # Hlavní FastAPI aplikace & endpointy
│   ├── models.py            # SQLAlchemy databázové modely
│   └── schemas.py           # Pydantic schémata pro validaci
├── .gitignore               # Konfigurace ignorovaných souborů pro Git
├── erp.db                   # SQLite databáze (vytvoří init_db.py)
├── init_db.py               # Skript pro inicializaci databáze
├── README.md                # Dokumentace projektu
└── requirements.txt         # Seznam závislostí
```

---

## 🛠️ Instalace a spuštění

Pro lokální zprovoznění projektu postupujte podle následujících kroků:

### 1. Klonování repozitáře
```bash
git clone <URL_TVÉHO_REPOZITÁŘE>
cd full-erp-example
```

### 2. Vytvoření a aktivace virtuálního prostředí
* **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalace závislostí
```bash
pip install -r requirements.txt
```

### 4. Inicializace databáze
Spusťte skript, který vytvoří databázové tabulky a vloží úvodní testovací data:
* **Windows:**
  ```powershell
  python init_db.py
  ```
* **macOS / Linux:**
  ```bash
  python3 init_db.py
  ```

### 5. Spuštění vývojového serveru Uvicorn
```bash
uvicorn app.main:app --reload
```

Aplikace bude následně dostupná na adresách:
* 🎨 **Uživatelské rozhraní:** `http://127.0.0.1:8000/products-ui`
* 📖 **API Dokumentace (Swagger):** `http://127.0.0.1:8000/docs`