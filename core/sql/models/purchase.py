from decimal import Decimal

from sqlmodel import Field, Relationship, SQLModel

from core.sql.models.base_model import BaseModel
from core.sql.models.purchase_product_link import PurchaseProductLink


class PurchaseBase(SQLModel):
    company_id: int = Field(default=None, foreign_key="company.id")


class Purchase(PurchaseBase, BaseModel, table=True):
    company: "Company" = Relationship(back_populates="purchases")  # noqa: F821
    products: list["Product"] = Relationship(  # noqa: F821
        back_populates="purchases",
        link_model=PurchaseProductLink,
    )
    products_purchased: list[PurchaseProductLink] = Relationship(
        back_populates="purchase",
    )


class PurchaseCreate(PurchaseBase):
    product_ids: list[int]


class PurchaseResponse(PurchaseBase):
    id: int
    products_purchased: list[PurchaseProductLink] = Field(
        default=[],
    )
    total: Decimal = Field(default=0, decimal_places=2)
