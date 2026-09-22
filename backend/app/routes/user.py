from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.user import (
    RegisterRequest,
    LoginRequest,
    ProfileUpdate,
    UserStatusUpdate,
)
from ..services.user import UserService
from .dependencies import current_user, require_roles

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "Registration successful",
        "data": UserService.create(db, data),
    }


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    u = UserService.authenticate(db, str(data.email), data.password)
    return {
        "success": True,
        "message": "Login successful",
        "token": UserService.token(u),
        "data": UserService.public(u),
    }


@router.get("/me")
def me(user=Depends(current_user)):
    return {"success": True, "data": UserService.public(user)}


@router.put("/me")
def update_me(
    data: ProfileUpdate, user=Depends(current_user), db: Session = Depends(get_db)
):
    return {
        "success": True,
        "message": "Profile updated successfully",
        "data": UserService.update_profile(db, user, data),
    }


@router.get("", dependencies=[Depends(require_roles("admin"))])
def users(db: Session = Depends(get_db)):
    items = UserService.list(db)
    return {"success": True, "count": len(items), "data": items}


@router.get("/{id}", dependencies=[Depends(require_roles("admin"))])
def user(id: int, db: Session = Depends(get_db)):
    return {"success": True, "data": UserService.public(UserService.get(db, id))}


@router.put("/{id}", dependencies=[Depends(require_roles("admin"))])
def update_user(id: int, data: ProfileUpdate, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "User updated successfully",
        "data": UserService.update(db, id, data),
    }


@router.patch("/{id}/status", dependencies=[Depends(require_roles("admin"))])
def status(id: int, data: UserStatusUpdate, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "User status updated successfully",
        "data": UserService.status(db, id, data.status),
    }
