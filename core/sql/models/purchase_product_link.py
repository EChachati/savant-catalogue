from decimal import Decimal

from sqlmodel import Field, Relationship

from core.sql.models.base_model import BaseModel


class PurchaseProductLink(BaseModel, table=True):
    purchase_id: int | None = Field(foreign_key="purchase.id")

    product_id: int | None = Field(foreign_key="product.id")

    quantity: int = Field(default=1)
    amount: Decimal = Field(default=0, decimal_places=2)
    purchase: "Purchase" = Relationship(back_populates="products_purchased")  # noqa: F821
