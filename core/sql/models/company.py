from sqlmodel import Relationship

from core.sql.mixins import NameMixin, PhoneMixin
from core.sql.models.base_model import BaseModel


class CompanyCreate(NameMixin, PhoneMixin):
    pass


class Company(CompanyCreate, BaseModel, table=True):
    products: list["Product"] = Relationship(back_populates="company")  # noqa: F821
    purchases: list["Purchase"] = Relationship(back_populates="company")  # noqa: F821
