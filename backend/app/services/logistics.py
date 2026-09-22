from datetime import datetime, timezone
from sqlalchemy import select
from ..exceptions.app_exception import AppException
from ..models.logistics import Logistics
from ..models.order import Order
from .helpers import entity_or_404


class LogisticsService:
    @staticmethod
    def create(db, data):
        order = entity_or_404(db, Order, data.orderId, "Order")
        if db.scalar(select(Logistics).where(Logistics.order_id == order.id)):
            raise AppException("Logistics record already exists for this order", 409)
        obj = Logistics(
            order_id=order.id,
            carrier=data.carrier.strip(),
            tracking_number=data.trackingNumber.strip(),
            shipping_address=data.shippingAddress.strip(),
            status=data.status,
            estimated_delivery=data.estimatedDelivery,
        )
        if obj.status == "shipped":
            obj.shipped_at = datetime.now(timezone.utc)
        if obj.status == "delivered":
            obj.delivered_at = datetime.now(timezone.utc)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def list(db, status=None):
        q = select(Logistics).order_by(Logistics.created_at.desc())
        if status:
            q = q.where(Logistics.status == status)
        return list(db.scalars(q).all())

    @staticmethod
    def get(db, id):
        return entity_or_404(db, Logistics, id, "Logistics")

    @staticmethod
    def update(db, id, data):
        obj = LogisticsService.get(db, id)
        mapping = {
            "carrier": "carrier",
            "trackingNumber": "tracking_number",
            "shippingAddress": "shipping_address",
            "status": "status",
            "estimatedDelivery": "estimated_delivery",
        }
        for source, target in mapping.items():
            value = getattr(data, source)
            if value is not None:
                setattr(obj, target, value.strip() if isinstance(value, str) else value)
        if obj.status == "shipped" and obj.shipped_at is None:
            obj.shipped_at = datetime.now(timezone.utc)
        if obj.status == "delivered" and obj.delivered_at is None:
            obj.delivered_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(obj)
        return obj
