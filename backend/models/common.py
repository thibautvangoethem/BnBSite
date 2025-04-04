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


class Dice(str, Enum):
    D2 = ("D2",)
    D4 = ("D4",)
    D6 = ("D6",)
    D8 = ("D8",)
    D10 = ("D10",)
    D12 = ("D12",)
    D20 = ("D20",)
    D100 = ("D100",)
