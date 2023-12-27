from datetime import datetime

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: int | None = Field(
        primary_key=True,
        index=True,
        default=None,
    )
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
