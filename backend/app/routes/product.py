from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.product import ProductCreate,ProductUpdate
from ..services.product import ProductService
from .dependencies import current_user,require_roles
router=APIRouter(prefix="/products",tags=["Products"])
@router.get("",dependencies=[Depends(current_user)])
def get_all(search:str|None=None,category:str|None=None,status:str|None=None,page:int=1,limit:int=10,db:Session=Depends(get_db)):
 items,total=ProductService.get_all(db,search,category,status,page,limit); return {"success":True,"count":total,"pages":max(1,(total+limit-1)//limit),"page":page,"data":items}
@router.post("",status_code=201,dependencies=[Depends(require_roles("admin"))])
def create(data:ProductCreate,db:Session=Depends(get_db)): return {"success":True,"message":"Product created successfully","data":ProductService.create(db,data)}
@router.get("/{id}",dependencies=[Depends(current_user)])
def get_one(id:int,db:Session=Depends(get_db)): return {"success":True,"data":ProductService.get_by_id(db,id)}
@router.put("/{id}",dependencies=[Depends(require_roles("admin","employee"))])
def update(id:int,data:ProductUpdate,db:Session=Depends(get_db)): return {"success":True,"message":"Product updated successfully","data":ProductService.update(db,id,data)}
@router.delete("/{id}",dependencies=[Depends(require_roles("admin"))])
def delete(id:int,db:Session=Depends(get_db)): return {"success":True,"message":"Product deactivated","data":ProductService.delete(db,id)}
