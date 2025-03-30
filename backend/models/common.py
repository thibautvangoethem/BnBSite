from enum import Enum


class Element(str, Enum):
    RADIATION = "Radiation"
    CORROSIVE = "Corrosive"
    SHOCK = "Shock"
    EXPLOSIVE = "Explosive"
    INCENDIARY = "Incendiary"
    CRYO = "Cryo"


class Manufacturer(str, Enum):
    ALAS = "Alas"
    SKULLDUGGER = "SkullDugger"
    DAHLIA = "Dahlia"
    BLACKPOWDER = "BlackPowder"
    MALEFACTOR = "MaleFactor"
    HYPERIUS = "Hyperius"
    FERIORE = "Feriore"
    TORGUE = "Torgue"
    STOKER = "Stoker"


class Rarity(str, Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    UNIQUE = "Unique"
