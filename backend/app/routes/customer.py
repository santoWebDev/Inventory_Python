from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.customer import CustomerCreate, CustomerUpdate
from ..services.customer import CustomerService
from .dependencies import current_user, require_roles

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", dependencies=[Depends(current_user)])
def get_all(
    search: str | None = None,
    status: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    items, total = CustomerService.get_all(db, search, status, page, limit)
    return {
        "success": True,
        "count": total,
        "pages": max(1, (total + limit - 1) // limit),
        "page": page,
        "data": items,
    }


@router.post(
    "", status_code=201, dependencies=[Depends(require_roles("admin", "employee"))]
)
def create(data: CustomerCreate, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "Customer created successfully",
        "data": CustomerService.create(db, data),
    }


@router.get("/{id}", dependencies=[Depends(current_user)])
def get_one(id: int, db: Session = Depends(get_db)):
    return {"success": True, "data": CustomerService.get(db, id)}


@router.put("/{id}", dependencies=[Depends(require_roles("admin", "employee"))])
def update(id: int, data: CustomerUpdate, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "Customer updated successfully",
        "data": CustomerService.update(db, id, data),
    }


@router.delete("/{id}", dependencies=[Depends(require_roles("admin"))])
def delete(id: int, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "Customer deactivated",
        "data": CustomerService.delete(db, id),
    }
