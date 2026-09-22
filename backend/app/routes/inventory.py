from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.inventory import StockInRequest, StockOutRequest, StockAdjustmentRequest
from ..services.inventory import InventoryService
from .dependencies import current_user, require_roles

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("/stock-in", dependencies=[Depends(require_roles("admin", "employee"))])
def stock_in(
    data: StockInRequest, user=Depends(current_user), db: Session = Depends(get_db)
):
    return {
        "success": True,
        "message": "Stock added successfully",
        "data": InventoryService.stock_in(db, user.id, data),
    }


@router.post("/stock-out", dependencies=[Depends(require_roles("admin", "employee"))])
def stock_out(
    data: StockOutRequest, user=Depends(current_user), db: Session = Depends(get_db)
):
    return {
        "success": True,
        "message": "Stock removed successfully",
        "data": InventoryService.stock_out(db, user.id, data),
    }


@router.post("/adjustment", dependencies=[Depends(require_roles("admin"))])
def adjustment(
    data: StockAdjustmentRequest,
    user=Depends(current_user),
    db: Session = Depends(get_db),
):
    return {
        "success": True,
        "message": "Stock adjusted successfully",
        "data": InventoryService.adjustment(db, user.id, data),
    }


@router.get(
    "/{product_id}/history", dependencies=[Depends(require_roles("admin", "employee"))]
)
def history(
    product_id: int, page: int = 1, limit: int = 20, db: Session = Depends(get_db)
):
    items, total = InventoryService.history(db, product_id, page, limit)
    return {
        "success": True,
        "count": total,
        "pages": max(1, (total + limit - 1) // limit),
        "page": page,
        "data": items,
    }
