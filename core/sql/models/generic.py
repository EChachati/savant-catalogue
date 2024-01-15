from decimal import Decimal

from sqlmodel import Field

from core.sql.mixins import NameMixin
from core.sql.models.base_model import BaseModel


class Currency(NameMixin, BaseModel, table=True):
    to_usd: Decimal = Field(default=0.0, decimal_places=2)
    symbol: str = Field(default="$", max_length=4)
    code: str = Field(default="USD", max_length=3)
