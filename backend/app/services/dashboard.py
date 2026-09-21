from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from ..models.product import Product
from ..models.category import Category
from ..models.supplier import Supplier
from ..models.order import Order
from ..models.customer import Customer
class DashboardService:
    @staticmethod
    def get(db):
        products=db.scalars(select(Product)).all(); orders=db.scalars(select(Order).order_by(Order.created_at.desc())).all()
        low=[p for p in products if p.status=="active" and p.stock>0 and p.stock<=p.low_stock_threshold]
        out=[p for p in products if p.status=="active" and p.stock==0]
        non_cancelled=[o for o in orders if o.status!="cancelled"]
        return {"products":{"total":len(products),"active":sum(p.status=="active" for p in products),"inactive":sum(p.status=="inactive" for p in products),"lowStock":len(low),"outOfStock":len(out)},"categories":{"total":db.scalar(select(func.count()).select_from(Category)) or 0,"active":db.scalar(select(func.count()).select_from(Category).where(Category.status=="active")) or 0},"suppliers":{"total":db.scalar(select(func.count()).select_from(Supplier)) or 0,"active":db.scalar(select(func.count()).select_from(Supplier).where(Supplier.status=="active")) or 0},"customers":{"total":db.scalar(select(func.count()).select_from(Customer)) or 0,"active":db.scalar(select(func.count()).select_from(Customer).where(Customer.status=="active")) or 0},"orders":{"total":len(orders),"pending":sum(o.status=="pending" for o in orders),"confirmed":sum(o.status=="confirmed" for o in orders),"shipped":sum(o.status=="shipped" for o in orders),"delivered":sum(o.status=="delivered" for o in orders),"cancelled":sum(o.status=="cancelled" for o in orders)},"sales":{"total":sum(o.total_amount for o in non_cancelled)},"recentOrders":orders[:5],"lowStockProducts":low[:10]}
