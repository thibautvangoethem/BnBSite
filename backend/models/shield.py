from typing import Optional
from sqlmodel import Field, SQLModel
from typing import Optional


class Shield(SQLModel, table=True):
    id: str = Field(primary_key=True)
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

    nova_damage: Optional[str]
    nova_element: Optional[str]

    model_config = {"from_attributes": True}

    def __str__(self):
        fields = [
            f"id={self.id}",
            f"name={self.name}" if self.name else None,
            f"description={self.description}" if self.description else None,
            f"rarity={self.rarity}",
            f"manufacturer={self.manufacturer}",
            f"capacity={self.capacity}",
            f"recharge_rate={self.recharge_rate}",
            f"recharge_delay={self.recharge_delay}",
            (
                f"manufacturer_effect={self.manufacturer_effect}"
                if self.manufacturer_effect
                else None
            ),
            (
                f"capacitor_effect={self.capacitor_effect}"
                if self.capacitor_effect
                else None
            ),
            f"battery_effect={self.battery_effect}" if self.battery_effect else None,
            f"red_text_name={self.red_text_name}" if self.red_text_name else None,
            (
                f"red_text_description={self.red_text_description}"
                if self.red_text_description
                else None
            ),
            f"nova_damage={self.nova_damage}" if self.nova_damage else None,
            f"nova_element={self.nova_element}" if self.nova_element else None,
        ]
        # Filter out None values and join the fields
        return f"Shield({', '.join(filter(None, fields))})"
