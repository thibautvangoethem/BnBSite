from pydantic import BaseModel
from models.common import Rarity, Classes
from sqlmodel import Field, SQLModel


# base pydantic model for creating a classmod
class ClassModCreate(BaseModel):
    rarity: Rarity
    class_type: Classes
    prefix: str
    prefix_effect: str
    suffix: str
    suffix_effect: str


class ClassMod(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    description: str
    rarity: Rarity
    class_type: Classes
    prefix: str
    prefix_effect: str
    suffix: str
    suffix_effect: str

    def __str__(self):
        fields = [
            f"id={self.id}",
            f"name={self.name}",
            f"description={self.description}",
            f"rarity={self.rarity.value}",
            f"class_type={self.class_type.value}",
            f"prefix={self.prefix}",
            f"prefix_effect={self.prefix_effect}",
            f"suffix={self.suffix}",
            f"suffix_effect={self.suffix_effect}",
        ]
        return f"ClassMod({', '.join(fields)})"
