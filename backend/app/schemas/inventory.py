from pydantic import BaseModel, Field
from .common import ORMModel
class StockInRequest(BaseModel):
    productId: int; quantity: int = Field(gt=0); reason: str = Field(min_length=1)
class StockOutRequest(StockInRequest): pass
class StockAdjustmentRequest(BaseModel):
    productId: int; newStock: int = Field(ge=0); reason: str = Field(min_length=1)
class TransactionResponse(ORMModel):
    id: int; product_id: int; quantity: int; type: str; previous_stock: int; new_stock: int; reason: str; reference_type: str; performed_by_id: int
