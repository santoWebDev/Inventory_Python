from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.logistics import LogisticsCreate, LogisticsUpdate
from ..services.logistics import LogisticsService
from .dependencies import require_roles, current_user

router = APIRouter(prefix="/logistics", tags=["Logistics"])


@router.get("", dependencies=[Depends(current_user)])
def get_all(status: str | None = None, db: Session = Depends(get_db)):
    return {"success": True, "data": LogisticsService.list(db, status)}


@router.post(
    "", status_code=201, dependencies=[Depends(require_roles("admin", "employee"))]
)
def create(data: LogisticsCreate, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "Logistics record created",
        "data": LogisticsService.create(db, data),
    }


@router.get("/{id}", dependencies=[Depends(current_user)])
def get_one(id: int, db: Session = Depends(get_db)):
    return {"success": True, "data": LogisticsService.get(db, id)}


@router.put("/{id}", dependencies=[Depends(require_roles("admin", "employee"))])
def update(id: int, data: LogisticsUpdate, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "Logistics updated",
        "data": LogisticsService.update(db, id, data),
    }
