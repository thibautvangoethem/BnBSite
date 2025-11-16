from sqlmodel import SQLModel, Field


class Potion(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    text: str | None = Field(default=None, index=True)

    def __str__(self):
        fields = [
            f"id={self.id}",
            f"name={self.name}" if self.name else None,
            f"text={self.text}" if self.text else None,
        ]
        # Filter out None values and join the fields
        return f"Potion({', '.join(filter(None, fields))})"
