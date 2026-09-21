from pydantic import BaseModel, Field

from .common import ORMModel


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    description: str = ""
    price: float = Field(ge=0)

    category_id: int
    supplier_id: int

    stock: int = Field(default=0, ge=0)
    low_stock_threshold: int = Field(default=10, ge=0)

    status: str = "active"


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, ge=0)

    category_id: int | None = None
    supplier_id: int | None = None

    stock: int | None = Field(default=None, ge=0)
    low_stock_threshold: int | None = Field(default=None, ge=0)

    status: str | None = None


class ProductResponse(ORMModel):
    id: int
    name: str
    description: str
    price: float

    category_id: int
    supplier_id: int

    stock: int
    status: str
    low_stock_threshold: int

    @property
    def _id(self):
        return self.id