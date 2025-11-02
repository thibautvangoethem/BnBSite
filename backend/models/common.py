from enum import Enum


class GunType(str, Enum):
    RIFLE = "Combat Rifle"
    SUBMACHINE = "Submachine gun"
    PISTOL = "Pistol"
    SHOTGUN = "Shotgun"
    SNIPER = "Sniper Rifle"
    ROCKET = "Rocket Launcher"


class Element(str, Enum):
    OEPS = "oepsikwasvergetendatgunsmeerelementskunnenhebbenennuzitdatnietinhetmodel"
    NIETS = "niets :("
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


class ManufacturerNormal(str, Enum):
    ATLAS = "Atlas"
    COV = "COV"
    DAHL = "Dahl"
    HYPERION = "Hyperion"
    JAKOBS = "Jakobs"
    MALIWAN = "Maliwan"
    TEDIORE = "Tediore"
    TORGUE = "Torgue"
    VLADOF = "Vladof"


class Rarity(str, Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    UNIQUE = "Unique"


class Dice(str, Enum):
    D2 = "D2"
    D4 = "D4"
    D6 = "D6"
    D8 = "D8"
    D10 = "D10"
    D12 = "D12"
    D20 = "D20"
    D100 = "D100"


class Classes(str, Enum):
    # Nick
    COMMANDO = "Commando"
    # jim
    HUNTER = "Hunter"
    # Thibaut
    GUNZERKER = "Gunzerker"
    # Owen
    BERSERKER = "Berseker"
    # Ruben
    PSYCHO = "Psycho"
    # Joren
    ASSASSIN = "Assassin"
    # Senne
    SIREN = "Siren"
    # Nog eens Nick, allez eigenlijk hebben we deze niet, maar past bij Nick
    MECHROMANCER = "Mechromancer"


ElementIndexed = {
    0: Element.RADIATION,
    1: Element.CORROSIVE,
    2: Element.SHOCK,
    3: Element.EXPLOSIVE,
    4: Element.INCENDIARY,
    5: Element.CRYO,
}

ManufacturerIndexed = {
    0: Manufacturer.SKULLDUGGER,
    1: Manufacturer.FERIORE,
    2: Manufacturer.DAHLIA,
    3: Manufacturer.BLACKPOWDER,
    4: Manufacturer.ALAS,
    5: Manufacturer.MALEFACTOR,
    6: Manufacturer.STOKER,
    7: Manufacturer.HYPERIUS,
    8: Manufacturer.TORGUE,
}

GunTypeIndexed = {
    0: GunType.PISTOL,
    1: GunType.SUBMACHINE,
    2: GunType.SHOTGUN,
    3: GunType.RIFLE,
    4: GunType.SNIPER,
    5: GunType.ROCKET,
}

RarityIndexed = {
    0: Rarity.COMMON,
    1: Rarity.UNCOMMON,
    2: Rarity.RARE,
    3: Rarity.EPIC,
    4: Rarity.LEGENDARY,
}

ClassIndexed = {
    0: Classes.COMMANDO,
    1: Classes.HUNTER,
    2: Classes.GUNZERKER,
    3: Classes.BERSERKER,
    4: Classes.PSYCHO,
    5: Classes.ASSASSIN,
    6: Classes.SIREN,
    7: Classes.MECHROMANCER,
}

ManufacturerMappedToNormal = {
    Manufacturer.ALAS: ManufacturerNormal.ATLAS,
    Manufacturer.SKULLDUGGER: ManufacturerNormal.COV,
    Manufacturer.DAHLIA: ManufacturerNormal.DAHL,
    Manufacturer.BLACKPOWDER: ManufacturerNormal.JAKOBS,
    Manufacturer.MALEFACTOR: ManufacturerNormal.MALIWAN,
    Manufacturer.HYPERIUS: ManufacturerNormal.HYPERION,
    Manufacturer.FERIORE: ManufacturerNormal.TEDIORE,
    Manufacturer.TORGUE: ManufacturerNormal.TORGUE,
    Manufacturer.STOKER: ManufacturerNormal.VLADOF,
}

NormalMappedToManufacturer = {
    ManufacturerNormal.ATLAS: Manufacturer.ALAS,
    ManufacturerNormal.COV: Manufacturer.SKULLDUGGER,
    ManufacturerNormal.DAHL: Manufacturer.DAHLIA,
    ManufacturerNormal.JAKOBS: Manufacturer.BLACKPOWDER,
    ManufacturerNormal.MALIWAN: Manufacturer.MALEFACTOR,
    ManufacturerNormal.HYPERION: Manufacturer.HYPERIUS,
    ManufacturerNormal.TEDIORE: Manufacturer.FERIORE,
    ManufacturerNormal.TORGUE: Manufacturer.TORGUE,
    ManufacturerNormal.VLADOF: Manufacturer.STOKER,
}
