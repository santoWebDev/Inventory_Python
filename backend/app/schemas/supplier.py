from pydantic import BaseModel, EmailStr, Field
from .common import ORMModel
class SupplierCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    number: str = Field(min_length=5, max_length=40)
    status: str = "active"
class SupplierUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None
    number: str | None = None
    status: str | None = None
class SupplierResponse(ORMModel):
    id: int; name: str; email: EmailStr; number: str; status: str
