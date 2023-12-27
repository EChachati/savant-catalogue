from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import SQLModel


class PhoneMixin(SQLModel):
    phone: PhoneNumber


class NameMixin(SQLModel):
    name: str
