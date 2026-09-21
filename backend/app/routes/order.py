from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.order import OrderCreate,OrderStatusUpdate,CancelRequest
from ..services.order import OrderService
from .dependencies import current_user,require_roles
router=APIRouter(prefix="/orders",tags=["Orders"])
@router.post("",dependencies=[Depends(require_roles("admin","employee"))])
def create(data:OrderCreate,user=Depends(current_user),db:Session=Depends(get_db)): return {"success":True,"message":"Order created successfully","data":OrderService.create(db,user.id,data)}
@router.get("",dependencies=[Depends(require_roles("admin"))])
def get_all(status:str|None=None,page:int=1,limit:int=10,db:Session=Depends(get_db)):
 items,total=OrderService.list(db,status,page,limit); return {"success":True,"count":total,"pages":max(1,(total+limit-1)//limit),"page":page,"data":items}
@router.get("/my-orders",dependencies=[Depends(require_roles("admin","employee"))])
def my_orders(status:str|None=None,page:int=1,limit:int=10,user=Depends(current_user),db:Session=Depends(get_db)):
 items,total=OrderService.list(db,status,page,limit,user.id); return {"success":True,"count":total,"pages":max(1,(total+limit-1)//limit),"page":page,"data":items}
@router.get("/{id}",dependencies=[Depends(require_roles("admin","employee"))])
def get_one(id:int,db:Session=Depends(get_db)): return {"success":True,"data":OrderService.get(db,id)}
@router.patch("/{id}/status",dependencies=[Depends(require_roles("admin"))])
def status(id:int,data:OrderStatusUpdate,db:Session=Depends(get_db)): return {"success":True,"message":"Order status updated","data":OrderService.update_status(db,id,data.status)}
@router.post("/{id}/cancel",dependencies=[Depends(require_roles("admin","employee"))])
def cancel(id:int,data:CancelRequest,db:Session=Depends(get_db)): return {"success":True,"message":"Order cancelled","data":OrderService.cancel(db,id,data.reason)}
