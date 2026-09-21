from pydantic import BaseModel, Field
from .common import ORMModel
class OrderItemCreate(BaseModel):
    productId: int; quantity: int = Field(gt=0)
class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1); customerId: int | None = None
class OrderStatusUpdate(BaseModel): status: str
class CancelRequest(BaseModel): reason: str = ""
class OrderItemResponse(ORMModel):
    id: int; product_id: int; name: str; price: float; quantity: int; subtotal: float
class OrderResponse(ORMModel):
    id: int; order_number: str; user_id: int; customer_id: int | None; total_amount: float; status: str; cancel_reason: str | None; items: list[OrderItemResponse]
