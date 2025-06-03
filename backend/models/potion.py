from sqlmodel import SQLModel, Field


class Potion(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    text: str | None = Field(default=None, index=True)
