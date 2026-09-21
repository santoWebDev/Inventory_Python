from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core.database import Base


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(20), index=True)
    previous_stock: Mapped[int] = mapped_column(Integer)
    new_stock: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(String(255))
    reference_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reference_type: Mapped[str] = mapped_column(String(20), default="MANUAL")
    performed_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    product = relationship("Product", back_populates="inventory_transactions")
    performed_by = relationship("User", back_populates="inventory_transactions")
