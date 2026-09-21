from sqlalchemy import func
from sqlalchemy.orm import Session
from ..exceptions.app_exception import AppException
from ..models.product import Product


def entity_or_404(db: Session, model, entity_id: int, label: str):
    obj = db.get(model, entity_id)
    if not obj:
        raise AppException(f"{label} not found", 404)
    return obj


def product_payload(product: Product):
    return {
        "id": product.id, "_id": product.id, "name": product.name, "description": product.description,
        "price": product.price, "category": product.category_id, "category_id": product.category_id,
        "supplier": product.supplier_id, "supplier_id": product.supplier_id, "stock": product.stock,
        "status": product.status, "lowStockThreshold": product.low_stock_threshold,
        "low_stock_threshold": product.low_stock_threshold,
    }
