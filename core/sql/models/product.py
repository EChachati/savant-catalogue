from decimal import Decimal

from pydantic import Field as PydanticField
from pydantic import field_validator
from sqlmodel import Field, Relationship

from core.api.category import crud as category_crud
from core.api.company import crud as company_crud
from core.sql.mixins import NameMixin
from core.sql.models.base_model import BaseModel
from core.sql.models.category import CategoryCreate
from core.sql.models.purchase_product_link import PurchaseProductLink


class ProductCreate(NameMixin):
    description: str = PydanticField(
        default="There is no description for this product.",
        max_length=500,
        min_length=2,
        examples=["Some Random Description"],
    )
    price: Decimal = Field(default=0.0, decimal_places=2)
    stock: Decimal = Field(default=0.0, decimal_places=2)

    barcode: str = PydanticField(
        ...,
        min_length=1,
        max_length=128,
        examples=["123456789"],
    )

    category_id: int | None = Field(default=None, foreign_key="category.id")
    company_id: int | None = Field(default=None, foreign_key="company.id")
    image: str | None = PydanticField(default=None, examples=["example.com"])

    @field_validator("description", mode="before")
    @classmethod
    def description_validations(cls, v):
        if v is None:
            return v.title()
        return v

    @field_validator("category_id", mode="before")
    @classmethod
    def category_validations(cls, v):
        if isinstance(v, str):
            return category_crud.get_or_create(
                CategoryCreate(**{"name": v.title()}),
                search_field="name",
            ).id
        return v

    @field_validator("company_id", mode="before")
    @classmethod
    def company_validations(cls, v):
        if isinstance(v, str):
            return company_crud.get_by_field_or_404(field="name", value=v).id
        return v


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
        from core.controllers.currency import get_ves_currency

        return Decimal(self.price * get_ves_currency().to_usd).quantize(
            Decimal("1.00")
        )


class ProductResponse(ProductCreate):
    id: int
    price_ves: Decimal = Field(default=0.0, decimal_places=2)
