    from datetime import datetime, timezone
    from sqlalchemy import func, select
    from sqlalchemy.orm import selectinload
    from ..exceptions.app_exception import AppException
    from ..models.order import Order, OrderItem
    from ..models.product import Product
    from ..models.customer import Customer
    from ..models.inventory import InventoryTransaction
    from .helpers import entity_or_404


    class OrderService:
        @staticmethod
        def create(db, user_id, data):
            customer = None
            if data.customerId:
                customer = entity_or_404(db, Customer, data.customerId, "Customer")
            order = Order(
                order_number=f"ORD-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[-10:]}",
                user_id=user_id,
                customer_id=customer.id if customer else None,
                status="pending",
                total_amount=0,
            )
            db.add(order)
            db.flush()
            total = 0
            for item in data.items:
                product = entity_or_404(db, Product, item.productId, "Product")
                if product.status != "active":
                    raise AppException(f"Product {product.name} is inactive", 400)
                if product.stock < item.quantity:
                    raise AppException(f"Insufficient stock for {product.name}", 400)
                subtotal = product.price * item.quantity
                total += subtotal
                previous = product.stock
                product.stock -= item.quantity
                order.items.append(
                    OrderItem(
                        product_id=product.id,
                        name=product.name,
                        price=product.price,
                        quantity=item.quantity,
                        subtotal=subtotal,
                    )
                )
                db.add(
                    InventoryTransaction(
                        product_id=product.id,
                        quantity=item.quantity,
                        type="OUT",
                        previous_stock=previous,
                        new_stock=product.stock,
                        reason=f"Order {order.order_number}",
                        reference_id=order.id,
                        reference_type="ORDER",
                        performed_by_id=user_id,
                    )
                )
            order.total_amount = total
            db.commit()
            db.refresh(order)
            return OrderService.get(db, order.id)

        @staticmethod
        def get(db, id):
            obj = db.scalar(
                select(Order).options(selectinload(Order.items)).where(Order.id == id)
            )
            if not obj:
                raise AppException("Order not found", 404)
            return obj

        @staticmethod
        def list(db, status=None, page=1, limit=10, user_id=None):
            q = (
                select(Order)
                .options(selectinload(Order.items))
                .order_by(Order.created_at.desc())
            )
            if status:
                q = q.where(Order.status == status)
            if user_id:
                q = q.where(Order.user_id == user_id)
            items = list(db.scalars(q).unique().all())
            total = len(items)
            start = (page - 1) * limit
            return items[start : start + limit], total

        @staticmethod
        def update_status(db, id, status):
            allowed = {"pending", "confirmed", "shipped", "delivered", "cancelled"}
            if status not in allowed:
                raise AppException("Invalid order status", 400)
            obj = OrderService.get(db, id)
            if obj.status == "cancelled":
                raise AppException("Cancelled order cannot be updated", 400)
            obj.status = status
            db.commit()
            db.refresh(obj)
            return obj

        @staticmethod
        def cancel(db, id, reason):
            obj = OrderService.get(db, id)
            if obj.status in ("delivered", "cancelled"):
                raise AppException("Order cannot be cancelled", 400)
            obj.status = "cancelled"
            obj.cancel_reason = reason.strip() or "Cancelled by user"
            obj.cancelled_at = datetime.now(timezone.utc)
            # Return quantities to inventory when an order is cancelled.
            for item in obj.items:
                p = db.get(Product, item.product_id)
                if p:
                    previous = p.stock
                    p.stock += item.quantity
                    db.add(
                        InventoryTransaction(
                            product_id=p.id,
                            quantity=item.quantity,
                            type="IN",
                            previous_stock=previous,
                            new_stock=p.stock,
                            reason=f"Cancellation {obj.order_number}",
                            reference_id=obj.id,
                            reference_type="ORDER",
                            performed_by_id=obj.user_id,
                        )
                    )
            db.commit()
            db.refresh(obj)
            return obj
