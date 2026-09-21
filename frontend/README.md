# Inventory Management Frontend

React + Vite + Tailwind frontend based on the supplied MERN inventory application's screens and flow, adapted to the FastAPI backend.

## Start

```powershell
npm install
copy .env.example .env
npm run dev
```

The `.env` should contain:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

New modules added to the original flow:
- Customers
- Logistics / fulfillment

The sidebar and dashboard were updated to expose these modules while keeping the original Products, Categories, Suppliers, Inventory, Orders, Users and Reports flow.
