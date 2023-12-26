from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Field, SQLModel


class IdMixin(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class PhoneMixin(SQLModel):
    phone: PhoneNumber


class NameMixin(SQLModel):
    name: str
