from pydantic import BaseModel, EmailStr, Field
from .common import ORMModel


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    role: str = "employee"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(ORMModel):
    id: int
    name: str
    email: EmailStr
    role: str
    status: str


class UserStatusUpdate(BaseModel):
    status: str
