from sqlalchemy import func, select
from ..exceptions.app_exception import AppException
from ..models.product import Product
from ..models.category import Category
from ..models.supplier import Supplier
from .helpers import entity_or_404, product_payload


class ProductService:
    @staticmethod
    def _validate_refs(db, category_id, supplier_id):
        if not db.get(Category, category_id):
            raise AppException("Category not found", 404)
        if not db.get(Supplier, supplier_id):
            raise AppException("Supplier not found", 404)

    @staticmethod
    def create(db, data):
        if db.scalar(
            select(Product).where(func.lower(Product.name) == data.name.strip().lower())
        ):
            raise AppException("Product already exists", 409)
        ProductService._validate_refs(db, data.category_id, data.supplier_id)
        obj = Product(
            name=data.name.strip(),
            description=data.description.strip(),
            price=data.price,
            category_id=data.category_id,
            supplier_id=data.supplier_id,
            stock=data.stock,
            low_stock_threshold=data.low_stock_threshold,
            status=data.status,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return product_payload(obj)

        @staticmethod
        def get_all(db, search=None, category=None, status=None, page=1, limit=10):
            q = select(Product).order_by(Product.created_at.desc())
            if search:
                q = q.where(Product.name.ilike(f"%{search}%"))
            if category:
                q = q.where(Product.category_id == int(category))
            if status:
                q = q.where(Product.status == status)
            all_items = list(db.scalars(q).all())
            total = len(all_items)
            start = (page - 1) * limit
            return [product_payload(x) for x in all_items[start : start + limit]], total

    @staticmethod
    def get_by_id(db, id):
        return product_payload(entity_or_404(db, Product, id, "Product"))

    @staticmethod
    def update(db, product_id, data):
        obj = db.get(Product, product_id)

        if not obj:
            raise AppException("Product not found", 404)

        # New value if supplied, otherwise existing value
        category_id = (
            data.category_id if data.category_id is not None else obj.category_id
        )

        supplier_id = (
            data.supplier_id if data.supplier_id is not None else obj.supplier_id
        )

        # Validate only the final IDs
        ProductService._validate_refs(db, category_id, supplier_id)

        if data.name is not None:
            obj.name = data.name

        if data.description is not None:
            obj.description = data.description

        if data.price is not None:
            obj.price = data.price

        if data.stock is not None:
            obj.stock = data.stock

        if data.category_id is not None:
            obj.category_id = data.category_id

        if data.supplier_id is not None:
            obj.supplier_id = data.supplier_id

        if data.low_stock_threshold is not None:
            obj.low_stock_threshold = data.low_stock_threshold

        if data.status is not None:
            obj.status = data.status

        db.commit()
        db.refresh(obj)

        return obj

    @staticmethod
    def delete(db, id):
        obj = entity_or_404(db, Product, id, "Product")
        obj.status = "inactive"
        db.commit()
        db.refresh(obj)
        return product_payload(obj)
