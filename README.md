# KiezMove

AI-powered moving-in concierge for Berlin.

KiezMove helps people navigate the practical tasks involved in
moving into a new home in Berlin.

The project focuses on making the moving-in process easier by
turning a user's situation into a personalized sequence of tasks.

---

## Current MVP

The current backend can:

- Create users.
- Store users in SQLite.
- Retrieve users through the API.
- Determine applicable moving-in tasks.
- Order tasks by priority.
- Determine the next incomplete task.
- Expose the functionality through FastAPI.
- Run automated tests with pytest.

AI agents and n8n orchestration will be added on top of this
foundation.

---

## Architecture

```text
User
 │
 ▼
Frontend
 │
 │ HTTP / JSON
 ▼
FastAPI
 │
 ├── Services
 │    ├── Eligibility
 │    └── Planner
 │
 ▼
SQLAlchemy
 │
 ▼
SQLite
```

---
## Project Structure
```text

kiezmove/
│
├── backend/
│   ├── app/
│   │   ├── database.py
│   │   ├── database_models.py
│   │   ├── init_db.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── test_db.py
│   │   │
│   │   └── services/
│   │       ├── eligibility.py
│   │       └── planner.py
│   │
│   └── data/
│       ├── sources.json
│       └── tasks.json
│
├── frontend/
│   └── app.py
│
├── n8n/
│   └── workflows/
│
├── tests/
│   ├── test_eligibility.py
│   └── test_planner.py
│
├── requirements.txt
├── README.md
└── .gitignore

```

---
## Local SetUp

1. Clone the repository
```
git clone <repository-url>
cd kiezmove
```
2. Create a virtual environment

```
Linux/macOS:        source .venv/bin/activate           
Windows:            .venv\Scripts\Activate.ps1   
```
4. Install dependencies
```
python -m pip install -r requirements.txt
```
5. Initialize the database
```
python -m backend.app.init_db
```

---
## Running Tests

```
python -m pytest
```
All test should pass before submitting changes

---
## Running the API
Start the development server

```
uvicorn backend.app.main:app --reload
```
The API will be available at:
```
http://127.0.0.1:8000
```
Open in browser
```
http://127.0.0.1:8000/docs
```

---
## Database

The local development database uses SQLite.
The database file is:

   kiezmove.db

It is intentionally excluded from Git.
Database structure is defined using SQLAlchemy models in:

    backend/app/database_models.py

To initialize the database:

    python -m backend.app.init_db
