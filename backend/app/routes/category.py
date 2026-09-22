from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from ..services.category import CategoryService
from .dependencies import current_user, require_roles

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", dependencies=[Depends(current_user)])
def get_categories(
    search: str | None = None, status: str | None = None, db: Session = Depends(get_db)
):
    return {
        "success": True,
        "count": len(CategoryService.get_all(db, search, status)),
        "data": CategoryService.get_all(db, search, status),
    }


@router.post("", status_code=201, dependencies=[Depends(require_roles("admin"))])
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    return {
        "success": True,
        "message": "Category created successfully",
        "data": CategoryService.create(db, data),
    }


@router.get("/{category_id}", dependencies=[Depends(current_user)])
def get_category(category_id: int, db: Session = Depends(get_db)):
    return {"success": True, "data": CategoryService.get_by_id(db, category_id)}


@router.put("/{category_id}", dependencies=[Depends(require_roles("admin"))])
def update_category(
    category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)
):
    return {
        "success": True,
        "message": "Category updated successfully",
        "data": CategoryService.update(db, category_id, data),
    }


@router.delete("/{category_id}", dependencies=[Depends(require_roles("admin"))])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return CategoryService.delete(db, category_id)
