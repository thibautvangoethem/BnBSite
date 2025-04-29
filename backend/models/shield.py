from enum import Enum
from models.common import Rarity, Manufacturer

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Shield(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: Optional[str]
    description: Optional[str] = None
    rarity: str
    manufacturer: str

    capacity: int
    recharge_rate: int
    recharge_delay: int = 1

    manufacturer_effect: str
    capacitor_effect: str
    battery_effect: str

    red_text: Optional[str]
