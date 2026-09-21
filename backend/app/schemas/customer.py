from pydantic import BaseModel, EmailStr, Field
from .common import ORMModel
class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120); email: EmailStr; phone: str = ""; address: str = ""; status: str = "active"
class CustomerUpdate(BaseModel):
    name: str | None = None; email: EmailStr | None = None; phone: str | None = None; address: str | None = None; status: str | None = None
class CustomerResponse(ORMModel):
    id: int; name: str; email: EmailStr; phone: str; address: str; status: str
