from enum import Enum
from models.common import Rarity, Manufacturerm, Classes
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel
from typing import Optional


class ClassMod(SQLModel, table=True):
    id: str = Field(primary_key=True)
    rarity: Rarity
    class_type: Classes
    prefix: str
    prefix_effect: str
    suffix: str
    suffix_effect: str
