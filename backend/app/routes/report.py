from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services.report import ReportService
from .dependencies import require_roles
router=APIRouter(prefix="/reports",tags=["Reports"])
@router.get("/sales",dependencies=[Depends(require_roles("admin"))])
def sales(db:Session=Depends(get_db)): return {"success":True,"data":ReportService.sales(db)}
@router.get("/inventory",dependencies=[Depends(require_roles("admin"))])
def inventory(db:Session=Depends(get_db)): return {"success":True,"data":ReportService.inventory(db)}
