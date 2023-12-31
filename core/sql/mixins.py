from pydantic import Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import SQLModel


class PhoneMixin(SQLModel):
    phone: PhoneNumber = Field(
        max_length=64,
        min_length=10,
        examples=["+584123456789"],
    )


class NameMixin(SQLModel):
    name: str = Field(
        max_length=100, min_length=2, examples=["Some Random Name"]
    )
