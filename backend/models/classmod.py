from models.common import Rarity, Classes
from sqlmodel import Field, SQLModel


class ClassMod(SQLModel, table=True):
    id: str = Field(primary_key=True)
    rarity: Rarity
    class_type: Classes
    prefix: str
    prefix_effect: str
    suffix: str
    suffix_effect: str
