from sqlalchemy import select
from ..exceptions.app_exception import AppException
from ..models.product import Product
from ..models.inventory import InventoryTransaction
from .helpers import entity_or_404, product_payload
class InventoryService:
    @staticmethod
    def _change(db,user_id,product_id,new_stock,quantity,kind,reason):
        product=entity_or_404(db,Product,product_id,"Product")
        if product.status!="active": raise AppException("Cannot update inactive product",400)
        previous=product.stock
        if new_stock<0: raise AppException("Stock cannot be negative",400)
        product.stock=new_stock
        tx=InventoryTransaction(product_id=product.id,quantity=quantity,type=kind,previous_stock=previous,new_stock=new_stock,reason=reason.strip(),reference_type="MANUAL",performed_by_id=user_id)
        db.add(tx); db.commit(); db.refresh(product); db.refresh(tx)
        return {"product":product_payload(product),"transaction":tx}
    @staticmethod
    def stock_in(db,user_id,data): return InventoryService._change(db,user_id,data.productId,entity_or_404(db,Product,data.productId,"Product").stock+data.quantity,data.quantity,"IN",data.reason)
    @staticmethod
    def stock_out(db,user_id,data):
        p=entity_or_404(db,Product,data.productId,"Product")
        if p.stock<data.quantity: raise AppException("Insufficient stock",400)
        return InventoryService._change(db,user_id,p.id,p.stock-data.quantity,data.quantity,"OUT",data.reason)
    @staticmethod
    def adjustment(db,user_id,data):
        p=entity_or_404(db,Product,data.productId,"Product")
        return InventoryService._change(db,user_id,p.id,data.newStock,abs(data.newStock-p.stock),"ADJUSTMENT",data.reason)
    @staticmethod
    def history(db,product_id,page=1,limit=20):
        q=select(InventoryTransaction).where(InventoryTransaction.product_id==product_id).order_by(InventoryTransaction.created_at.desc())
        items=list(db.scalars(q).all()); total=len(items); start=(page-1)*limit
        return items[start:start+limit],total
