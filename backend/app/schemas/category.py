from pydantic import BaseModel, Field
from .common import ORMModel

class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = ""

class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None
    status: str | None = None

class CategoryResponse(ORMModel):
    id: int; name: str; description: str; status: str
