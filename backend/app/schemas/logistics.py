from datetime import datetime
from pydantic import BaseModel
from .common import ORMModel
class LogisticsCreate(BaseModel):
    orderId: int; carrier: str = ""; trackingNumber: str = ""; shippingAddress: str = ""; status: str = "pending"; estimatedDelivery: datetime | None = None
class LogisticsUpdate(BaseModel):
    carrier: str | None = None; trackingNumber: str | None = None; shippingAddress: str | None = None; status: str | None = None; estimatedDelivery: datetime | None = None
class LogisticsResponse(ORMModel):
    id: int; order_id: int; carrier: str; tracking_number: str; shipping_address: str; status: str; estimated_delivery: datetime | None; shipped_at: datetime | None; delivered_at: datetime | None
