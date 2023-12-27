from decimal import Decimal

from sqlmodel import Field, Relationship

from core.sql.mixins import NameMixin
from core.sql.models.base_model import BaseModel
from core.sql.models.purchase_product_link import PurchaseProductLink


class ProductCreate(NameMixin):
    description: str
    price: Decimal = Field(default=0.0, decimal_places=2)
    image: str

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
