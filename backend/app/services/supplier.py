from sqlalchemy import func, select
from ..exceptions.app_exception import AppException
from ..models.supplier import Supplier
from .helpers import entity_or_404
class SupplierService:
    @staticmethod
    def create(db,data):
        if db.scalar(select(Supplier).where(func.lower(Supplier.name)==data.name.strip().lower())): raise AppException("Supplier name already exists",409)
        if db.scalar(select(Supplier).where(func.lower(Supplier.email)==str(data.email).lower())): raise AppException("Supplier email already exists",409)
        obj=Supplier(name=data.name.strip(),email=str(data.email).lower(),number=data.number.strip(),status=data.status)
        db.add(obj); db.commit(); db.refresh(obj); return obj
    @staticmethod
    def get_all(db,search=None,status=None,page=1,limit=10):
        q=select(Supplier).order_by(Supplier.created_at.desc())
        if search: q=q.where(Supplier.name.ilike(f"%{search}%") | Supplier.email.ilike(f"%{search}%") | Supplier.number.ilike(f"%{search}%"))
        if status: q=q.where(Supplier.status==status)
        items=list(db.scalars(q).all()); total=len(items); start=(page-1)*limit
        return items[start:start+limit], total
    @staticmethod
    def get_by_id(db,id): return entity_or_404(db,Supplier,id,"Supplier")
    @staticmethod
    def update(db,id,data):
        obj=SupplierService.get_by_id(db,id)
        for field in ("name","email","number","status"):
            value=getattr(data,field)
            if value is not None: setattr(obj,field,str(value).strip().lower() if field=="email" else str(value).strip())
        db.commit(); db.refresh(obj); return obj
    @staticmethod
    def delete(db,id):
        obj=SupplierService.get_by_id(db,id); obj.status="inactive"; db.commit(); db.refresh(obj); return obj
