from sqlmodel import Relationship

from core.sql.mixins import NameMixin
from core.sql.models.base_model import BaseModel


class CategoryCreate(NameMixin):
    pass


class Category(CategoryCreate, BaseModel, table=True):
    products: list["Product"] = Relationship(back_populates="category")  # noqa: F821
