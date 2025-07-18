from enum import Enum
from models.common import Rarity, Manufacturer

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel
from typing import Optional


class Grenade(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: Optional[str]
    description: Optional[str] = None
    rarity: Rarity
    manufacturer: Manufacturer

    manufacturer_effect: Optional[str]
    primer_effect: Optional[str]
    detonater_effect: Optional[str]

    red_text_name: Optional[str]
    red_text_description: Optional[str]

    damage: Optional[str]
    radius: Optional[str]

    model_config = {"from_attributes": True}


# class ShieldRead(BaseModel):
#     name: Optional[str]
#     description: Optional[str]
#     rarity: str
#     manufacturer: str
#     capacity: int
#     recharge_rate: int
#     recharge_delay: int
#     manufacturer_effect: Optional[str]
#     capacitor_effect: Optional[str]
#     battery_effect: Optional[str]
#     red_text: Optional[str]

#     model_config = {"from_attributes": True}
