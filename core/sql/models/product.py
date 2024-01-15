from decimal import Decimal

from pydantic import Field as PydanticField
from sqlmodel import Field, Relationship

from core.controllers.currency import CurrencyController
from core.sql.mixins import NameMixin
from core.sql.models.base_model import BaseModel
from core.sql.models.purchase_product_link import PurchaseProductLink


class ProductCreate(NameMixin):
    description: str = PydanticField(
        max_length=500,
        min_length=2,
        examples=["Some Random Description"],
    )
    price: Decimal = Field(default=0.0, decimal_places=2)
    image: str | None = PydanticField(default=None, examples=["example.com"])

    category_id: int | None = Field(default=None, foreign_key="category.id")
    company_id: int | None = Field(default=None, foreign_key="company.id")


class Product(ProductCreate, BaseModel, table=True):
    category: "Category" = Relationship(back_populates="products")  # noqa: F821
    company: "Company" = Relationship(back_populates="products")  # noqa: F821

    purchases: list["Purchase"] = Relationship(  # noqa: F821
        back_populates="products",
        link_model=PurchaseProductLink,
    )

    links: list[PurchaseProductLink] = Relationship(back_populates="product")

    @property
    def price_ves(self):
        ves_to_usd_value = CurrencyController().get_by_code("VES").to_usd
        return Decimal(self.price * ves_to_usd_value).quantize(Decimal("1.00"))


class ProductResponse(ProductCreate):
    price_ves: Decimal = Field(default=0.0, decimal_places=2)
