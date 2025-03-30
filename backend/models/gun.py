from enum import Enum
from models.common import Element, Manufacturer, Rarity
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class GunType(str, Enum):
    RIFLE = "Combat Rifle"
    SUBMACHINE = "Submachine gun"
    PISTOl = "Pistol"
    SHOTGUN = "Shotgun"
    SNIPER = "Sniper Rifle"


class GunPrefixLink(SQLModel, table=True):
    gun_id: Optional[str] = Field(default=None, foreign_key="gun.id", primary_key=True)
    prefix_id: Optional[str] = Field(
        default=None, foreign_key="prefix.id", primary_key=True
    )


class GunPostfixLink(SQLModel, table=True):
    gun_id: Optional[str] = Field(default=None, foreign_key="gun.id", primary_key=True)
    postfix_id: Optional[str] = Field(
        default=None, foreign_key="postfix.id", primary_key=True
    )


class Gun(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    description: Optional[str] = None
    type: GunType
    rarity: Rarity
    manufacturer: Manufacturer
    manufacturer_effect: Optional[str] = None
    element: Optional[str] = None

    range: int
    lowNormal: int
    lowCrit: int
    mediumNormal: int
    mediumCrit2: int
    highNormal: int
    highCrit: int

    # Relationship to Prefix through the association table
    prefixes: List["Prefix"] = Relationship(
        back_populates="guns", link_model=GunPrefixLink
    )

    postfixes: List["Postfix"] = Relationship(
        back_populates="guns", link_model=GunPostfixLink
    )


class Prefix(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    effect: str

    # Relationship to Gun through the association table
    guns: List[Gun] = Relationship(back_populates="prefixes", link_model=GunPrefixLink)


class Postfix(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    effect: str

    # Relationship to Gun through the association table
    guns: List[Gun] = Relationship(
        back_populates="postfixes", link_model=GunPostfixLink
    )


Gun.model_rebuild()
Prefix.model_rebuild()
Postfix.model_rebuild()
