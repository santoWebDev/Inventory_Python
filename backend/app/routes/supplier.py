from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.supplier import SupplierCreate, SupplierUpdate
from ..services.supplier import SupplierService
from .dependencies import current_user, require_roles

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.get("", dependencies=[Depends(current_user)])
def get_all(
    search: str | None = None,
    status: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    items, total = SupplierService.get_all(db, search, status, page, limit)
    return {
        "success": True,
        "count": total,
        "pages": max(1, (total + limit - 1) // limit),
        "page": page,
        "data": items,
    }


@router.post("", status_code=201, dependencies=[Depends(require_roles("admin"))])
def create(data: SupplierCreate, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "Supplier created successfully",
        "data": SupplierService.create(db, data),
    }


@router.get("/{id}", dependencies=[Depends(current_user)])
def get_one(id: int, db: Session = Depends(get_db)):
    return {"success": True, "data": SupplierService.get_by_id(db, id)}


@router.put("/{id}", dependencies=[Depends(require_roles("admin", "employee"))])
def update(id: int, data: SupplierUpdate, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "Supplier updated successfully",
        "data": SupplierService.update(db, id, data),
    }


@router.delete("/{id}", dependencies=[Depends(require_roles("admin"))])
def delete(id: int, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "Supplier deactivated",
        "data": SupplierService.delete(db, id),
    }
