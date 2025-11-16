from models.common import *
from typing import Optional
from sqlmodel import Field, SQLModel


class Gun(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    description: Optional[str] = None
    type: GunType
    rarity: Rarity
    manufacturer: Manufacturer
    manufacturer_effect: Optional[str] = None
    element: Optional[Element] = None
    elementstr: Optional[str] = None

    range: int
    dmgroll: str
    lowNormal: int
    lowCrit: int
    mediumNormal: int
    mediumCrit: int
    highNormal: int
    highCrit: int

    # als den Arne later dit als lijst wilt dan pas ik dat wel aan
    redtext_name: str
    redtext_effect: str

    prefix_name: str
    prefix_effect: str

    barrel_manufacturer: ManufacturerNormal
    barrel_effect: str
    magazine_manufacturer: ManufacturerNormal
    magazine_effect: str
    grip_manufacturer: ManufacturerNormal
    grip_effect: str
    match_bonus: Optional[str] = None

    def __str__(self):
        fields = [
            f"id= {self.id}",
            f"name= {self.name}",
            f"description= {self.description}",
            f"type= {self.type.value}",
            f"rarity= {self.rarity.value}",
            f"manufacturer= {self.manufacturer.value}",
            f"manufacturer_effect= {self.manufacturer_effect}",
            f"element= {self.element}",
            f"elementstr= {self.elementstr}",
            f"range= {self.range}",
            f"dmgroll= {self.dmgroll}",
            f"lowNormal= {self.lowNormal}",
            f"lowCrit= {self.lowCrit}",
            f"mediumNormal= {self.mediumNormal}",
            f"mediumCrit= {self.mediumCrit}",
            f"highNormal= {self.highNormal}",
            f"highCrit= {self.highCrit}",
        ]
        return f"gun({', '.join(filter(None, fields))})"


#     prefixes: List[Prefix] = Relationship(
#         back_populates="guns", link_model=GunPrefixLink
#     )

#     postfixes: List[Postfix] = Relationship(
#         back_populates="guns", link_model=GunPostfixLink
#     )

#     redtexts: List[RedText] = Relationship(
#         back_populates="guns", link_model=GunRedTextLink
#     )


# Prefix.model_rebuild()
# Postfix.model_rebuild()
# Gun.model_rebuild()
