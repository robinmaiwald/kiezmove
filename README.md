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




| Method  | Endpoint                           | Purpose                                 |
| ------- | ---------------------------------- | --------------------------------------- |
| `GET`   | `/health`                          | Check that the API is running           |
| `GET`   | `/tasks`                           | Get all reusable task definitions       |
| `POST`  | `/users`                           | Create a new user                       |
| `GET`   | `/users/{user_id}`                 | Get a user's profile                    |
| `POST`  | `/users/{user_id}/tasks`           | Create/initialize that user's task plan |
| `GET`   | `/users/{user_id}/tasks`           | Get the user's task plan                |
| `PATCH` | `/users/{user_id}/tasks/{task_id}` | Change a task's status                  |
| `GET`   | `/users/{user_id}/next-task`       | Get the user's next incomplete task     |










```mermaid
flowchart TD
    A["POST /users"] --> B["Create user"]
    B --> C["POST /users/{id}/tasks"]
    C --> D["Eligibility rules"]
    D --> E["Create UserTask records"]
    E --> F["GET /users/{id}/tasks"]
    F --> G["User sees their task plan"]
    G --> H["GET /users/{id}/next-task"]
    H --> I["Planner finds next incomplete task"]
    I --> J["PATCH /users/{id}/tasks/{task_id}"]
    J --> K["Mark task completed/pending"]
    K --> H