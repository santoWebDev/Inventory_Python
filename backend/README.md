# Inventory Management System - FastAPI Backend

## Architecture

`routes -> schemas -> services -> models -> database`

- **routes/** = HTTP only. Receives request, gets DB session/current user, calls a service, returns the service result.
- **schemas/** = Pydantic request/response validation.
- **services/** = business logic. Functions such as duplicate checks, stock calculations, order totals, status rules and soft-delete decisions live here.
- **models/** = SQLAlchemy database tables and relationships.
- **exceptions/** = application errors and one global FastAPI error handler.
- **core/** = database connection and application settings.

## PostgreSQL

The project is configured for the existing pgAdmin database named `inventory_db`.

1. Make sure PostgreSQL is running.
2. In `backend/.env`, set your actual PostgreSQL username/password.
3. The database itself must already exist. This project creates missing tables automatically when the API starts.
4. `Base.metadata.create_all()` does not migrate/alter an already-existing table. If your existing tables have a different schema, use a migration tool such as Alembic later.

## Start backend on Windows

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# edit .env with your PostgreSQL password
uvicorn app.main:app --reload --port 8000
```

Open:
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## First login

Register an account through `/api/users/register`. The register endpoint defaults to the `employee` role. For a development admin account, change the role in the database or add a seed script later.

Example SQL in pgAdmin:

```sql
UPDATE users SET role = 'admin' WHERE email = 'your-email@example.com';
```

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

Create `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```
