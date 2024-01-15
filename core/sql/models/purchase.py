from decimal import Decimal

from sqlmodel import Field, Relationship, SQLModel

from core.controllers.currency import CurrencyController
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
    def total_usd(self):
        return sum([link.amount for link in self.products_purchased])

    @property
    def total_bcv(self):
        ves_to_usd_value = CurrencyController().get_by_code("VES").to_usd
        return Decimal(self.total_usd * ves_to_usd_value).quantize(
            Decimal("1.00")
        )

    def as_message(self):
        purchase = f"Pedido #{self.id}\n\n"
        product_label = "Productos:\n\t"
        products = "".join(
            [
                f"\n👉 {item.product.name} x{item.quantity}"
                for item in self.products_purchased
            ]
        )
        total = f"\n\nTotal:\n\t$ {self.total_usd}\n\tBs. {self.total_bcv}"

        return purchase + product_label + products + total


class PurchaseCreate(PurchaseBase):
    product_ids: list[int]


class PurchaseResponse(PurchaseBase):
    id: int
    products_purchased: list[PurchaseProductLink] = Field(default=[])
    total_usd: Decimal = Field(default=0.0, decimal_places=2)
    total_bcv: Decimal = Field(default=0.0, decimal_places=2)
