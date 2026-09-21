from sqlalchemy import select
from ..models.product import Product
from ..models.order import Order
class ReportService:
    @staticmethod
    def sales(db):
        orders=list(db.scalars(select(Order).order_by(Order.created_at.desc())).all())
        valid=[o for o in orders if o.status!="cancelled"]
        return {"totalSales":sum(o.total_amount for o in valid),"totalOrders":len(valid),"orders":valid}
    @staticmethod
    def inventory(db):
        products=list(db.scalars(select(Product).order_by(Product.created_at.desc())).all())
        return {"totalProducts":len(products),"totalStock":sum(p.stock for p in products),"lowStock":sum(p.stock>0 and p.stock<=p.low_stock_threshold for p in products),"outOfStock":sum(p.stock==0 for p in products),"products":products}
