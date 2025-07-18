from sqlmodel import SQLModel, Field

from datetime import datetime


class RollHistory(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    type: str = Field(index=True)
    date: datetime | None = Field(default=None, index=True)
    description: str = Field(index=False)
