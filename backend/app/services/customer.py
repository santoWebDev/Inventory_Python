from sqlalchemy import func, select
from ..exceptions.app_exception import AppException
from ..models.customer import Customer
from .helpers import entity_or_404
class CustomerService:
    @staticmethod
    def create(db,data):
        if db.scalar(select(Customer).where(func.lower(Customer.email)==str(data.email).lower())): raise AppException("Customer email already exists",409)
        obj=Customer(name=data.name.strip(),email=str(data.email).lower(),phone=data.phone.strip(),address=data.address.strip(),status=data.status)
        db.add(obj); db.commit(); db.refresh(obj); return obj
    @staticmethod
    def get_all(db,search=None,status=None,page=1,limit=10):
        q=select(Customer).order_by(Customer.created_at.desc())
        if search: q=q.where(Customer.name.ilike(f"%{search}%")|Customer.email.ilike(f"%{search}%")|Customer.phone.ilike(f"%{search}%"))
        if status: q=q.where(Customer.status==status)
        all_items=list(db.scalars(q).all()); total=len(all_items); start=(page-1)*limit
        return all_items[start:start+limit],total
    @staticmethod
    def get(db,id): return entity_or_404(db,Customer,id,"Customer")
    @staticmethod
    def update(db,id,data):
        obj=CustomerService.get(db,id)
        for f in ("name","email","phone","address","status"):
            v=getattr(data,f)
            if v is not None: setattr(obj,f,str(v).lower() if f=="email" else str(v).strip())
        db.commit(); db.refresh(obj); return obj
    @staticmethod
    def delete(db,id):
        obj=CustomerService.get(db,id); obj.status="inactive"; db.commit(); db.refresh(obj); return obj
