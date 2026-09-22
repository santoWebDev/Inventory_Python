from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services.dashboard import DashboardService
from .dependencies import require_roles

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", dependencies=[Depends(require_roles("admin"))])
def dashboard(db: Session = Depends(get_db)):
    return {"success": True, "data": DashboardService.get(db)}
