from decimal import Decimal

from sqlmodel import Field, Relationship, SQLModel

from core.sql.mixins import IdMixin, NameMixin, PhoneMixin


class CompanyCreate(PhoneMixin, NameMixin):
    pass


class Company(CompanyCreate, IdMixin, table=True):
    products: list["Product"] = Relationship(back_populates="company")
    purchases: list["Purchase"] = Relationship(back_populates="company")


class CategoryCreate(NameMixin):
    pass


class Category(CategoryCreate, IdMixin, table=True):
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

    quantity: int = Field(default=1)
    amount: Decimal = Field(default=0, decimal_places=2)
    purchase: "Purchase" = Relationship(back_populates="products_purchased")


class ProductCreate(NameMixin):
    description: str
    price: Decimal = Field(default=0, decimal_places=2)
    image: str

    category_id: int | None = Field(default=None, foreign_key="category.id")
    company_id: int | None = Field(default=None, foreign_key="company.id")


class Product(ProductCreate, IdMixin, table=True):
    category: Category = Relationship(back_populates="products")
    company: Company = Relationship(back_populates="products")
    purchases: list["Purchase"] = Relationship(
        back_populates="products",
        link_model=PurchaseProductLink,
    )


class PurchaseBase(SQLModel):
    company_id: int = Field(default=None, foreign_key="company.id")


class Purchase(PurchaseBase, IdMixin, table=True):
    company: Company = Relationship(back_populates="purchases")
    products: list[Product] = Relationship(
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
        alias="products",
    )
    total: Decimal = Field(default=0, decimal_places=2)
