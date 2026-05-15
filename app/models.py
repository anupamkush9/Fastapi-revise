from datetime import datetime

from sqlmodel import SQLModel, Field


class Blog(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)

    title: str = Field(max_length=150)

    description: str

    image: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
