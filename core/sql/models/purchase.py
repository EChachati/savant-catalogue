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

    @property
    def total(self):
        return sum([link.amount for link in self.products_purchased])

    def as_message(self):
        purchase = f"Pedido {self.id}\n\n"
        product_label = "Productos:\n\t"
        products = "".join(
            [
                f"\n👉 {item.product.name} x{item.quantity}"
                for item in self.products_purchased
            ]
        )
        total = f"\n\nTotal: $ {self.total}"

        return purchase + product_label + products + total


class PurchaseCreate(PurchaseBase):
    product_ids: list[int]


class PurchaseResponse(PurchaseBase):
    id: int
    products_purchased: list[PurchaseProductLink] = Field(default=[])
    total: Decimal = Field(default=0.0, decimal_places=2)
