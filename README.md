# Inventory Management System - Python Full Stack

This project is a Python full-stack conversion of the supplied MERN inventory project.

## Stack
- Frontend: React, Vite, Tailwind CSS, Axios
- Backend: FastAPI, SQLAlchemy 2.0, Pydantic
- Database: PostgreSQL (`inventory_db`)
- Auth: JWT + bcrypt

## Backend architecture

```text
backend/app/
├── models/       # database tables
├── schemas/      # request/response validation
├── services/     # BUSINESS LOGIC
├── routes/       # HTTP ONLY
├── exceptions/   # custom errors + global handler
├── core/         # database + config
└── main.py
```

`dashboard.py` and `report.py` are supporting service/route modules required to preserve the dashboard/report flow present in the supplied MERN application. Customers and Logistics were added as first-class modules.

## Important business-logic examples

- `services/category.py` -> duplicate name checks, update rules, product-aware soft delete.
- `services/product.py` -> duplicate checks, category/supplier validation, product update rules.
- `services/inventory.py` -> stock-in/out/adjustment calculations and inventory transaction creation.
- `services/order.py` -> order total calculation, stock validation, stock deduction, cancellation/restocking.
- `services/customer.py` -> customer duplicate validation and status handling.
- `services/logistics.py` -> shipment creation and tracking status timestamps.

Routes deliberately do not contain these rules; they call the service methods.

See `backend/README.md` for the exact PostgreSQL/pgAdmin startup steps.
