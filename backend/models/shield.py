from enum import Enum
from models.common import Rarity, Manufacturer

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel
from typing import Optional


class Shield(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: Optional[str]
    description: Optional[str] = None
    rarity: str
    manufacturer: str

    capacity: int
    recharge_rate: int
    recharge_delay: int = 1

    manufacturer_effect: Optional[str]
    capacitor_effect: Optional[str]
    battery_effect: Optional[str]

    red_text_name: Optional[str]
    red_text_description: Optional[str]


class ShieldRead(BaseModel):
    name: Optional[str]
    description: Optional[str]
    rarity: str
    manufacturer: str
    capacity: int
    recharge_rate: int
    recharge_delay: int
    manufacturer_effect: Optional[str]
    capacitor_effect: Optional[str]
    battery_effect: Optional[str]

    red_text_name: Optional[str]
    red_text_description: Optional[str]

    model_config = {"from_attributes": True}
