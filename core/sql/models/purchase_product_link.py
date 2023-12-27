from decimal import Decimal

from sqlmodel import Field, Relationship

from core.sql.models.base_model import BaseModel


class PurchaseProductLink(BaseModel, table=True):
    purchase_id: int | None = Field(
        default=None,
        foreign_key="purchase.id",
        primary_key=True,
    )

    product_id: int | None = Field(
        default=None,
        foreign_key="product.id",
        primary_key=True,
    )

    quantity: int = Field(default=1)
    amount: Decimal = Field(default=0, decimal_places=2)
    purchase: "Purchase" = Relationship(back_populates="products_purchased")  # noqa: F821
