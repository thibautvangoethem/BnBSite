from enum import Enum
from models.common import *
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class GunPrefixLink(SQLModel, table=True):
    gun_id: Optional[str] = Field(default=None, foreign_key="gun.id", primary_key=True)
    prefix_id: Optional[int] = Field(
        default=None, foreign_key="prefix.id", primary_key=True
    )


class GunPostfixLink(SQLModel, table=True):
    gun_id: Optional[str] = Field(default=None, foreign_key="gun.id", primary_key=True)
    postfix_id: Optional[int] = Field(
        default=None, foreign_key="postfix.id", primary_key=True
    )


class GunRedTextLink(SQLModel, table=True):
    gun_id: Optional[str] = Field(default=None, foreign_key="gun.id", primary_key=True)
    redtext_id: Optional[int] = Field(
        default=None, foreign_key="redtext.id", primary_key=True
    )


class Prefix(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    effect: str

    # Relationship to Gun through the association table
    guns: List["Gun"] = Relationship(
        back_populates="prefixes", link_model=GunPrefixLink
    )


class Postfix(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    effect: str

    # Relationship to Gun through the association table
    guns: List["Gun"] = Relationship(
        back_populates="postfixes", link_model=GunPostfixLink
    )


class RedText(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    effect: str

    # Relationship to Gun through the association table
    guns: List["Gun"] = Relationship(
        back_populates="redtexts", link_model=GunRedTextLink
    )


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

    def __str__(self):
        fields = [
            f"id= {self.id}",
            f"name= {self.name}",
            f"description= {self.description}",
            f"type= {self.type}",
            f"rarity= {self.rarity}",
            f"manufacturer= {self.manufacturer}",
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

    prefixes: List[Prefix] = Relationship(
        back_populates="guns", link_model=GunPrefixLink
    )

    postfixes: List[Postfix] = Relationship(
        back_populates="guns", link_model=GunPostfixLink
    )

    redtexts: List[RedText] = Relationship(
        back_populates="guns", link_model=GunRedTextLink
    )


Prefix.model_rebuild()
Postfix.model_rebuild()
Gun.model_rebuild()
