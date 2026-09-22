from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ..exceptions.app_exception import AppException
from ..models.category import Category
from ..models.product import Product


class CategoryService:
    @staticmethod
    def create(db: Session, data):
        name = data.name.strip()
        if db.scalar(select(Category).where(func.lower(Category.name) == name.lower())):
            raise AppException("Category already exists", 409)
        obj = Category(name=name, description=data.description.strip())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_all(db, search=None, status=None):
        q = select(Category).order_by(Category.created_at.desc())
        if search:
            q = q.where(Category.name.ilike(f"%{search}%"))
        if status:
            q = q.where(Category.status == status)
        return list(db.scalars(q).all())

    @staticmethod
    def get_by_id(db, id):
        obj = db.get(Category, id)
        if not obj:
            raise AppException("Category not found", 404)
        return obj

    @staticmethod
    def update(db, id, data):
        obj = CategoryService.get_by_id(db, id)
        if data.name is not None:
            name = data.name.strip()
            if db.scalar(
                select(Category).where(
                    func.lower(Category.name) == name.lower(), Category.id != id
                )
            ):
                raise AppException("Category name already exists", 409)
            obj.name = name
        if data.description is not None:
            obj.description = data.description
        if data.status is not None:
            if data.status not in ("active", "inactive"):
                raise AppException("Invalid category status", 400)
            obj.status = data.status
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def delete(db, id):
        obj = CategoryService.get_by_id(db, id)
        if db.scalar(select(Product.id).where(Product.category_id == id).limit(1)):
            obj.status = "inactive"
            db.commit()
            db.refresh(obj)
            return {
                "success": True,
                "message": "Category has products, so it was marked inactive",
                "data": obj,
            }
        db.delete(obj)
        db.commit()
        return {"success": True, "message": "Category deleted successfully"}
