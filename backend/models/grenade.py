from enum import Enum
from models.common import Rarity, Manufacturer

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel
from typing import Optional


class GrenadeCreate(BaseModel):
    rarity: Rarity
    manufacturer: Manufacturer

    manufacturer_effect: str
    primer_effect: str
    detonater_effect: str

    red_text_name: Optional[str]
    red_text_description: Optional[str]

    damage: str
    radius: str


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

    def __str__(self):
        fields = [
            f"id={self.id}",
            f"name={self.name}" if self.name else None,
            f"description={self.description}" if self.description else None,
            f"rarity={self.rarity.value}",
            f"manufacturer={self.manufacturer.value}",
            (
                f"manufacturer_effect={self.manufacturer_effect}"
                if self.manufacturer_effect
                else None
            ),
            f"primer_effect={self.primer_effect}" if self.primer_effect else None,
            (
                f"detonater_effect={self.detonater_effect}"
                if self.detonater_effect
                else None
            ),
            f"red_text_name={self.red_text_name}" if self.red_text_name else None,
            (
                f"red_text_description={self.red_text_description}"
                if self.red_text_description
                else None
            ),
            f"damage={self.damage}" if self.damage else None,
            f"radius={self.radius}",
        ]
        # Filter out None values and join the fields
        return f"Grenade({', '.join(filter(None, fields))})"


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
