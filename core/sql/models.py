from decimal import Decimal

from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Field, Relationship, SQLModel


class CompanyCreate(SQLModel):
    name: str
    phone: PhoneNumber


class Company(CompanyCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)
    products: list["Product"] = Relationship(back_populates="company")
    purchases: list["Purchase"] = Relationship(back_populates="company")


class CategoryCreate(SQLModel):
    name: str


class Category(CategoryCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)
    products: list["Product"] = Relationship(back_populates="category")


class PurchaseProductLink(SQLModel, table=True):
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


class ProductCreate(SQLModel):
    name: str
    description: str
    price: Decimal = Field(default=0, decimal_places=2)
    image: str

    category_id: int | None = Field(default=None, foreign_key="category.id")
    company_id: int | None = Field(default=None, foreign_key="company.id")


class Product(ProductCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category: Category = Relationship(back_populates="products")
    company: Company = Relationship(back_populates="products")
    purchases: list["Purchase"] = Relationship(
        back_populates="products",
        link_model=PurchaseProductLink,
    )


class PurchaseBase(SQLModel):
    amount: Decimal = Field(default=0, decimal_places=2)
    company_id: int | None = Field(default=None, foreign_key="company.id")


class Purchase(PurchaseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    company: Company = Relationship(back_populates="purchases")
    products: list[Product] = Relationship(
        back_populates="purchases",
        link_model=PurchaseProductLink,
    )


class PurchaseCreate(PurchaseBase):
    product_ids: list[int]
