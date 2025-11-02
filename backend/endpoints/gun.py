from datetime import datetime
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from models.rollhistory import RollHistory
from models.gun import *
from models.common import *
from appglobals import SessionDep, oauth2_scheme
from sqlmodel import select
from sqlalchemy.orm import selectinload
from models.roll_data import *
from uuid import uuid4
import random


import uuid

router = APIRouter(
    prefix="/guns",
    tags=["guns"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# custom creation of gun
class GunCreate(BaseModel):
    name: str
    description: Optional[str] = None
    guntype: GunType
    rarity: Rarity
    manufacturer: Manufacturer
    manufacturer_effect: Optional[str] = None
    element: Optional[Element] = None
    elementstr: Optional[str] = None
    prefix_ids: List[int] = []
    postfix_ids: List[int] = []
    redtext_ids: List[int] = []

    range: int
    dmgroll: str
    lowNormal: int
    lowCrit: int
    mediumNormal: int
    mediumCrit: int
    highNormal: int
    highCrit: int


# sad sqlmodel werkt niet deftig met foreign keys
class GunResponse(BaseModel):
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

    prefixes: List[Prefix]

    postfixes: List[Postfix]

    redtexts: List[RedText]


@router.get("/")
def read_guns(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Gun]:
    guns = session.exec(select(Gun).offset(offset).limit(limit)).all()
    return guns


@router.get("/rolldescription", response_model=random_create_description)
def get_create_descritpion_test(session: SessionDep) -> random_create_description:
    description = random_create_description(
        level=True,
        selections=selection_descriptions(
            mandatory=[
                selection_description(
                    label="favoured_manufacturer",
                    options=[member.value for member in Manufacturer],
                ),
                selection_description(
                    label="favoured_guns",
                    options=[member.value for member in GunType],
                ),
            ],
            optional=[
                selection_description(
                    label="rarity",
                    options=[member.value for member in Rarity],
                ),
                selection_description(
                    label="enforce_manufacturer",
                    options=[member.value for member in Manufacturer],
                ),
                selection_description(
                    label="enforce_guntype",
                    options=[member.value for member in GunType],
                ),
            ],
        ),
        rolls=rollswrapper(
            entries=[
                roll_description(label="Gun roll", diceList=[Dice.D8, Dice.D8]),
                roll_description(label="Rarity roll", diceList=[Dice.D4, Dice.D6]),
                roll_description(label="Element roll", diceList=[Dice.D100]),
                roll_description(label="Prefix", diceList=[Dice.D20]),
                roll_description(label="Redtext", diceList=[Dice.D100]),
                roll_description(
                    label="Parts", diceList=[Dice.D100, Dice.D20, Dice.D100]
                ),
            ],
            uuid=str(uuid4()),
        ),
    )
    return description


gunmask = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [0, 2, 0, 1, 2, 3, 4, 5],
    [-1, -1, -1, -1, -1, -1, -1, -1],
]
manufacturerMask = [
    [0, 1, 2, 3, 4, 5, 6, 7],
    [5, 0, 7, 1, 8, 2, 0, 1],
    [7, 3, 0, 1, 8, 6, 4, 8],
    [1, 2, 8, 6, 7, 4, 2, 4],
    [0, 4, 3, 5, 2, 7, 6, 8],
    [6, 8, 5, 7, 6, 8, 5, 7],
    [8, 2, 3, 0, 3, 1, 3, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
]

rarityMask = [
    [0, 0, 0, 1, 1, 2],
    [0, 0, 1, 1, 2, 3],
    [1, 2, 2, 3, 3, 4],
    [2, 2, 3, 3, 4, 4],
]

elementalRolMask = [
    [False, True, True, False, True, False],
    [False, True, False, True, True, False],
    [True, False, True, False, True, True],
    [True, True, True, True, True, True],
]
# 1 is never elemental., 1 is always elemental and 0 is normal flow (based on rarity roll)
guildElementalOverrideMask = {
    Manufacturer.SKULLDUGGER: 0,
    Manufacturer.FERIORE: 0,
    Manufacturer.DAHLIA: 0,
    Manufacturer.BLACKPOWDER: -1,
    Manufacturer.ALAS: -1,
    Manufacturer.MALEFACTOR: 1,
    Manufacturer.STOKER: 0,
    Manufacturer.HYPERIUS: 0,
    Manufacturer.TORGUE: 0,
}

guildRarityBonusMap = {
    Manufacturer.SKULLDUGGER: {
        Rarity.COMMON: "+2 DMG Mod, Overheat: 1d4",
        Rarity.UNCOMMON: "+3 DMG Mod, Overheat: 1d6",
        Rarity.RARE: "+4 DMG Mod, Overheat: 1d8",
        Rarity.EPIC: "+5 DMG Mod, Overheat: 1d10",
        Rarity.LEGENDARY: "+6 DMG Mod, Overheat: 1d12",
    },
    Manufacturer.FERIORE: {
        Rarity.COMMON: "Swap/Reload: 1d4 Grenade Damage, –3 ACC Mod",
        Rarity.UNCOMMON: "Swap/Reload: 1d6 Grenade Damage, –3 ACC Mod",
        Rarity.RARE: "Swap/Reload: 1d8 Grenade Damage, –2 ACC Mod",
        Rarity.EPIC: "Swap/Reload: 1d10 Grenade Damage, –2 ACC Mod",
        Rarity.LEGENDARY: "Swap/Reload: 1d12 Grenade Damage, –1 ACC Mod",
    },
    Manufacturer.DAHLIA: {
        Rarity.COMMON: "Burst: +1 Hit",
        Rarity.UNCOMMON: "Burst: +1 Hit, +1 ACC Mod",
        Rarity.RARE: "Burst: +1 Hit, +2 ACC Mod",
        Rarity.EPIC: "Burst: +1 Hit, +3 ACC Mod",
        Rarity.LEGENDARY: "Burst: +1 Hit, +4 ACC Mod",
    },
    Manufacturer.BLACKPOWDER: {
        Rarity.COMMON: "+2 ACC Mod, +2 Crit Damage",
        Rarity.UNCOMMON: "+2 ACC Mod, +3 Crit Damage",
        Rarity.RARE: "+2 ACC Mod, +4 Crit Damage",
        Rarity.EPIC: "+2 ACC Mod, +5 Crit Damage",
        Rarity.LEGENDARY: "+2 ACC Mod, +6 Crit Damage",
    },
    Manufacturer.ALAS: {
        Rarity.COMMON: "+1 DMG Mod",
        Rarity.UNCOMMON: "+2 DMG Mod",
        Rarity.RARE: "+3 DMG Mod",
        Rarity.EPIC: "+3 DMG Mod",
        Rarity.LEGENDARY: "+4 DMG Mod",
    },
    Manufacturer.MALEFACTOR: {
        Rarity.COMMON: "Element Roll, –2 DMG Mod",
        Rarity.UNCOMMON: "Element Roll, –1 DMG Mod",
        Rarity.RARE: "+10% Element Roll",
        Rarity.EPIC: "+15% Element Roll",
        Rarity.LEGENDARY: "+20% Element Roll",
    },
    Manufacturer.STOKER: {
        Rarity.COMMON: "Extra Attack, –3 ACC Mod",
        Rarity.UNCOMMON: "Extra Attack, –2 ACC Mod",
        Rarity.RARE: "Extra Attack, –1 ACC Mod",
        Rarity.EPIC: "Extra Attack",
        Rarity.LEGENDARY: "Extra Attack, Extra Movement",
    },
    Manufacturer.HYPERIUS: {
        Rarity.COMMON: "+1 ACC Mod, –2 DMG Mod",
        Rarity.UNCOMMON: "+2 ACC Mod, –2 DMG Mod",
        Rarity.RARE: "+3 ACC Mod, –2 DMG Mod",
        Rarity.EPIC: "+4 ACC Mod, –2 DMG Mod",
        Rarity.LEGENDARY: "+5 ACC Mod, –2 DMG Mod",
    },
    Manufacturer.TORGUE: {
        Rarity.COMMON: "Splash, –4 ACC Mod",
        Rarity.UNCOMMON: "Splash, –3 ACC Mod",
        Rarity.RARE: "Splash, –2 ACC Mod",
        Rarity.EPIC: "Splash, –1 ACC Mod",
        Rarity.LEGENDARY: "Splash",
    },
}

# en God weende op de 8ste dag
elementalRarityRolArray = [
    {
        "range": [1, 10],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.NIETS, "N/A"],
            Rarity.RARE: [Element.NIETS, "N/A"],
            Rarity.EPIC: [Element.NIETS, "N/A"],
            Rarity.LEGENDARY: [Element.NIETS, "N/A"],
        },
    },
    {
        "range": [11, 15],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.NIETS, "N/A"],
            Rarity.RARE: [Element.NIETS, "N/A"],
            Rarity.EPIC: [Element.RADIATION, "Radiation"],
            Rarity.LEGENDARY: [Element.RADIATION, "Radiation"],
        },
    },
    {
        "range": [16, 20],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.NIETS, "N/A"],
            Rarity.RARE: [Element.NIETS, "N/A"],
            Rarity.EPIC: [Element.CORROSIVE, "Corrosive"],
            Rarity.LEGENDARY: [Element.CORROSIVE, "Corrosive"],
        },
    },
    {
        "range": [21, 25],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.NIETS, "N/A"],
            Rarity.RARE: [Element.NIETS, "N/A"],
            Rarity.EPIC: [Element.SHOCK, "Shock"],
            Rarity.LEGENDARY: [Element.SHOCK, "Shock"],
        },
    },
    {
        "range": [26, 30],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.NIETS, "N/A"],
            Rarity.RARE: [Element.RADIATION, "Radiation"],
            Rarity.EPIC: [Element.EXPLOSIVE, "Explosive"],
            Rarity.LEGENDARY: [Element.EXPLOSIVE, "Explosive"],
        },
    },
    {
        "range": [31, 35],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.NIETS, "N/A"],
            Rarity.RARE: [Element.CORROSIVE, "Corrosive"],
            Rarity.EPIC: [Element.INCENDIARY, "Incendiary"],
            Rarity.LEGENDARY: [Element.INCENDIARY, "Incendiary"],
        },
    },
    {
        "range": [36, 40],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.NIETS, "N/A"],
            Rarity.RARE: [Element.SHOCK, "Shock"],
            Rarity.EPIC: [Element.CRYO, "Cryo"],
            Rarity.LEGENDARY: [Element.CRYO, "Cryo"],
        },
    },
    {
        "range": [41, 45],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.NIETS, "N/A"],
            Rarity.RARE: [Element.EXPLOSIVE, "Explosive"],
            Rarity.EPIC: [Element.RADIATION, "Radiation (+1d6)"],
            Rarity.LEGENDARY: [Element.RADIATION, "Radiation (+1d6)"],
        },
    },
    {
        "range": [46, 50],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.NIETS, "N/A"],
            Rarity.RARE: [Element.INCENDIARY, "Incendiary"],
            Rarity.EPIC: [Element.CORROSIVE, "Corrosive (+1d6)"],
            Rarity.LEGENDARY: [Element.CORROSIVE, "Corrosive (+1d6)"],
        },
    },
    {
        "range": [51, 55],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.NIETS, "N/A"],
            Rarity.RARE: [Element.CRYO, "Cryo"],
            Rarity.EPIC: [Element.SHOCK, "Shock (+1d6)"],
            Rarity.LEGENDARY: [Element.SHOCK, "Shock (+1d6)"],
        },
    },
    {
        "range": [56, 60],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.RADIATION, "Radiation"],
            Rarity.RARE: [Element.RADIATION, "Radiation (+1d6)"],
            Rarity.EPIC: [Element.EXPLOSIVE, "Explosive (+1d6)"],
            Rarity.LEGENDARY: [Element.EXPLOSIVE, "Explosive (+1d6)"],
        },
    },
    {
        "range": [61, 65],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.CORROSIVE, "Corrosive"],
            Rarity.RARE: [Element.CORROSIVE, "Corrosive (+1d6)"],
            Rarity.EPIC: [Element.INCENDIARY, "Incendiary (+1d6)"],
            Rarity.LEGENDARY: [Element.INCENDIARY, "Incendiary (+1d6)"],
        },
    },
    {
        "range": [66, 70],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.SHOCK, "Shock"],
            Rarity.RARE: [Element.SHOCK, "Shock (+1d6)"],
            Rarity.EPIC: [Element.CRYO, "Cryo (+1d6)"],
            Rarity.LEGENDARY: [Element.CRYO, "Cryo (+1d6)"],
        },
    },
    {
        "range": [71, 75],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.EXPLOSIVE, "Explosive"],
            Rarity.RARE: [Element.EXPLOSIVE, "Explosive (+1d6)"],
            Rarity.EPIC: [Element.RADIATION, "Radiation (+2d6)"],
            Rarity.LEGENDARY: [Element.RADIATION, "Radiation (+2d6)"],
        },
    },
    {
        "range": [76, 80],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.INCENDIARY, "Incendiary"],
            Rarity.RARE: [Element.INCENDIARY, "Incendiary (+1d6)"],
            Rarity.EPIC: [Element.CORROSIVE, "Corrosive (+2d6)"],
            Rarity.LEGENDARY: [Element.CORROSIVE, "Corrosive (+2d6)"],
        },
    },
    {
        "range": [81, 85],
        "rarity": {
            Rarity.COMMON: [Element.NIETS, "N/A"],
            Rarity.UNCOMMON: [Element.CRYO, "Cryo"],
            Rarity.RARE: [Element.CRYO, "Cryo (+1d6)"],
            Rarity.EPIC: [Element.SHOCK, "Shock (+2d6)"],
            Rarity.LEGENDARY: [Element.SHOCK, "Shock (+2d6)"],
        },
    },
    {
        "range": [86, 90],
        "rarity": {
            Rarity.COMMON: [Element.RADIATION, "Radiation"],
            Rarity.UNCOMMON: [Element.RADIATION, "Radiation (+1d6)"],
            Rarity.RARE: [Element.RADIATION, "Radiation (+2d6)"],
            Rarity.EPIC: [Element.EXPLOSIVE, "Explosive (+2d6)"],
            Rarity.LEGENDARY: [Element.EXPLOSIVE, "Explosive (+2d6)"],
        },
    },
    {
        "range": [91, 92],
        "rarity": {
            Rarity.COMMON: [Element.CORROSIVE, "Corrosive"],
            Rarity.UNCOMMON: [Element.CORROSIVE, "Corrosive (+1d6)"],
            Rarity.RARE: [Element.CORROSIVE, "Corrosive (+2d6)"],
            Rarity.EPIC: [Element.INCENDIARY, "Incendiary (+2d6)"],
            Rarity.LEGENDARY: [Element.INCENDIARY, "Incendiary (+2d6)"],
        },
    },
    {
        "range": [93, 94],
        "rarity": {
            Rarity.COMMON: [Element.SHOCK, "Shock"],
            Rarity.UNCOMMON: [Element.SHOCK, "Shock (+1d6)"],
            Rarity.RARE: [Element.SHOCK, "Shock (+2d6)"],
            Rarity.EPIC: [Element.CRYO, "Cryo (+2d6)"],
            Rarity.LEGENDARY: [Element.CRYO, "Cryo (+2d6)"],
        },
    },
    {
        "range": [95, 96],
        "rarity": {
            Rarity.COMMON: [Element.EXPLOSIVE, "Explosive"],
            Rarity.UNCOMMON: [Element.EXPLOSIVE, "Explosive (+1d6)"],
            Rarity.RARE: [Element.EXPLOSIVE, "Explosive (+2d6)"],
            Rarity.EPIC: [Element.OEPS, "Radiation + Incendiary"],
            Rarity.LEGENDARY: [Element.OEPS, "Radiation + Incendiary"],
        },
    },
    {
        "range": [97, 98],
        "rarity": {
            Rarity.COMMON: [Element.INCENDIARY, "Incendiary"],
            Rarity.UNCOMMON: [Element.INCENDIARY, "Incendiary (+1d6)"],
            Rarity.RARE: [Element.INCENDIARY, "Incendiary (+2d6)"],
            Rarity.EPIC: [Element.OEPS, "Shock + Corrosive"],
            Rarity.LEGENDARY: [Element.OEPS, "Shock + Corrosive"],
        },
    },
    {
        "range": [99, 100],
        "rarity": {
            Rarity.COMMON: [Element.CRYO, "Cryo"],
            Rarity.UNCOMMON: [Element.CRYO, "Cryo (+1d6)"],
            Rarity.RARE: [Element.CRYO, "Cryo (+2d6)"],
            Rarity.EPIC: [Element.OEPS, "Explosive + Cryo"],
            Rarity.LEGENDARY: [Element.OEPS, "Explosive + Cryo"],
        },
    },
]

gunRangeMap = {
    GunType.RIFLE: 6,
    GunType.PISTOL: 5,
    GunType.SUBMACHINE: 5,
    GunType.SHOTGUN: 4,
    GunType.SNIPER: 8,
    GunType.ROCKET: 4,
}

# tis map: guns => [levels ,[[hits],damage die]]
damageMap = {
    GunType.RIFLE: [
        [[1, 6], [[1, 0, 3, 0, 3, 1], "1d6"]],
        [[7, 12], [[2, 0, 3, 0, 2, 1], "1d8"]],
        [[13, 18], [[1, 1, 2, 1, 2, 2], "1d8"]],
        [[19, 24], [[1, 0, 2, 1, 3, 1], "2d6"]],
        [[25, 30], [[1, 1, 2, 1, 2, 3], "1d10"]],
    ],
    GunType.PISTOL: [
        [[1, 6], [[1, 0, 2, 0, 3, 0], "2d4"]],
        [[7, 12], [[1, 0, 1, 1, 3, 1], "1d6"]],
        [[13, 18], [[1, 0, 2, 0, 2, 1], "2d6"]],
        [[19, 24], [[1, 0, 1, 1, 1, 2], "2d8"]],
        [[25, 30], [[2, 0, 2, 1, 2, 2], "2d8"]],
    ],
    GunType.SUBMACHINE: [
        [[1, 6], [[2, 0, 3, 0, 5, 0], "1d4"]],
        [[7, 12], [[2, 0, 4, 0, 5, 1], "2d4"]],
        [[13, 18], [[2, 0, 3, 1, 5, 1], "1d6"]],
        [[19, 24], [[2, 0, 2, 1, 4, 1], "2d6"]],
        [[25, 30], [[2, 2, 3, 2, 5, 2], "1d10"]],
    ],
    GunType.SHOTGUN: [
        [[1, 6], [[1, 0, 2, 0, 1, 1], "1d8"]],
        [[7, 12], [[1, 0, 2, 0, 2, 1], "2d8"]],
        [[13, 18], [[1, 1, 2, 1, 2, 2], "2d8"]],
        [[19, 24], [[1, 0, 1, 1, 2, 1], "2d10"]],
        [[25, 30], [[1, 1, 2, 1, 2, 2], "1d12"]],
    ],
    GunType.SNIPER: [
        [[1, 6], [[0, 0, 1, 0, 1, 1], "1d10"]],
        [[7, 12], [[0, 0, 1, 0, 1, 1], "1d12"]],
        [[13, 18], [[1, 0, 1, 1, 1, 2], "1d10"]],
        [[19, 24], [[1, 0, 1, 1, 1, 2], "2d10"]],
        [[25, 30], [[1, 0, 1, 1, 2, 2], "1d12"]],
    ],
    GunType.ROCKET: [
        [[1, 6], [[1, 0, 1, 0, 1, 1], "1d12"]],
        [[7, 12], [[1, 0, 1, 0, 1, 1], "2d10"]],
        [[13, 18], [[1, 0, 1, 0, 1, 2], "1d12"]],
        [[19, 24], [[1, 0, 1, 0, 2, 1], "2d12"]],
        [[25, 30], [[1, 1, 1, 1, 2, 1], "1d20"]],
    ],
}

grip_data = {
    ManufacturerNormal.ATLAS: {
        GunType.RIFLE: "1 RANGE",
        GunType.SUBMACHINE: "1 RANGE",
        GunType.PISTOL: "-1 recoil",
        GunType.SHOTGUN: "1 SPD, 1 MST",
        GunType.SNIPER: "2 RANGE, 3 RECOIL",
        GunType.ROCKET: "2 RANGE, -1 SPD",
    },
    ManufacturerNormal.COV: {
        GunType.RIFLE: "-1 ACC, 1 DMG",
        GunType.SUBMACHINE: "1 HIT, -2 ACC, RELOAD ON 3 OR LESS",
        GunType.PISTOL: "+1 Damage, +1 recoil",
        GunType.SHOTGUN: "2 DMG, 2 RECOIL",
        GunType.SNIPER: "2 RECOIL, 1 SPD",
        GunType.ROCKET: "-2 ACC, +1 MELEE DAMAGE DIE",
    },
    ManufacturerNormal.DAHL: {
        GunType.RIFLE: "-1 DMG, -1 RECOIL",
        GunType.SUBMACHINE: "1 ACC, -1 DMG",
        GunType.PISTOL: "+1 ACC",
        GunType.SHOTGUN: "1 ACC, -1 DMG",
        GunType.SNIPER: "-2 DMG, -2 RECOIL",
        GunType.ROCKET: "1 ACC, -1 DMG",
    },
    ManufacturerNormal.HYPERION: {
        GunType.RIFLE: "2 ACC, -2 DMG",
        GunType.SUBMACHINE: "-2 DAMAGE, +2 ACC",
        GunType.PISTOL: "+2 ACC first attack per turn",
        GunType.SHOTGUN: "-1 DMG, 1 ACC",
        GunType.SNIPER: "2 ACC, -2 DMG",
        GunType.ROCKET: "2 ACC, -2 DMG",
    },
    ManufacturerNormal.JAKOBS: {
        GunType.RIFLE: "2 DMG, 2 RECOIL, 2 CRIT DAMAGE",
        GunType.SUBMACHINE: "-4 ACC, 2 CRIT DMG",
        GunType.PISTOL: "+2 Crit damage, +3 recoil",
        GunType.SHOTGUN: "2 DMG, 2 RECOIL",
        GunType.SNIPER: "4 DMG, 4 RECOIL, -4 ACC",
        GunType.ROCKET: "2 DMG, 2 CRIT DAMAGE, 5 RECOIL",
    },
    ManufacturerNormal.MALIWAN: {
        GunType.RIFLE: "1 ELEMENTEL DAMAGE DIE",
        GunType.SUBMACHINE: "1 ELEMENTAL DAMAGE DIE",
        GunType.PISTOL: "+1 ACC on elemental guns",
        GunType.SHOTGUN: "1 MST, +1 ELEMENTAL DAMAGE DIE",
        GunType.SNIPER: "2 MST, 2 RECOIL",
        GunType.ROCKET: "1 ELEMENTAL DAMAGE DIE",
    },
    ManufacturerNormal.TEDIORE: {
        GunType.RIFLE: "-1 ACC, -1 RECOIL",
        GunType.SUBMACHINE: "-1 DMG",
        GunType.PISTOL: "on reload, +2 ACC next attack, +1 recoil",
        GunType.SHOTGUN: "-1 DMG",
        GunType.SNIPER: "2 ACC, -4 DMG",
        GunType.ROCKET: "-2 DMG, -1 ACC, +2 MST",
    },
    ManufacturerNormal.TORGUE: {
        GunType.RIFLE: "2 DAMAGE, -1 ACCURACY, 2 RECOIL",
        GunType.SUBMACHINE: "1 DMG",
        GunType.PISTOL: "+2 Damage, +2 recoil",
        GunType.SHOTGUN: "2 DMG, 4 RECOIL",
        GunType.SNIPER: "2 DMG, -2 RECOIL",
        GunType.ROCKET: "4 DAMAGE, -3 ACC, 2 RECOIL",
    },
    ManufacturerNormal.VLADOF: {
        GunType.RIFLE: "1 HITS, -2 DMG",
        GunType.SUBMACHINE: "2 SPD",
        GunType.PISTOL: "+1 ACC, +1 Recoil",
        GunType.SHOTGUN: "-5 ACC, +1 HIT",
        GunType.SNIPER: "1 SPD, -1 ACC",
        GunType.ROCKET: "1 HITS, 1 SPD, 2 RECOIL",
    },
}

barrel_data = {
    ManufacturerNormal.ATLAS: {
        GunType.RIFLE: "+2 Range, +1 ACC",
        GunType.SUBMACHINE: "+2 Range, -1 DMG",
        GunType.PISTOL: "+1 Range",
        GunType.SHOTGUN: "Always Full Damage",
        GunType.SNIPER: "+2 Range, +2 Recoil",
        GunType.ROCKET: "+1 Range, +1 ACC",
    },
    ManufacturerNormal.COV: {
        GunType.RIFLE: "+1 DMG, -1 ACC",
        GunType.SUBMACHINE: "+1 DMG, -1 ACC",
        GunType.PISTOL: "+1 DMG, +1 Recoil",
        GunType.SHOTGUN: "+1 DMG, -1 ACC, +1 Recoil",
        GunType.SNIPER: "-2 ACC, +2 Damage",
        GunType.ROCKET: "+2 DMG, -2 ACC",
    },
    ManufacturerNormal.DAHL: {
        GunType.RIFLE: "+1 ACC, -1 Recoil, -1 DMG",
        GunType.SUBMACHINE: "-1 Recoil",
        GunType.PISTOL: "+1 Range, +1 Recoil",
        GunType.SHOTGUN: "+1 ACC",
        GunType.SNIPER: "-2 Recoil",
        GunType.ROCKET: "+1 ACC, -1 DMG",
    },
    ManufacturerNormal.HYPERION: {
        GunType.RIFLE: "+2 ACC, -2 DMG",
        GunType.SUBMACHINE: "+2 ACC, -1 DMG",
        GunType.PISTOL: "+1 ACC, discard recoil on crit (roll of 20)",
        GunType.SHOTGUN: "+1 ACC, -1 DMG, -1 Recoil",
        GunType.SNIPER: "+1 ACC, -1 Recoil",
        GunType.ROCKET: "+2 ACC, -3 DMG",
    },
    ManufacturerNormal.JAKOBS: {
        GunType.RIFLE: "+2 DMG, +3 Recoil",
        GunType.SUBMACHINE: "+2 DMG, +2 Recoil",
        GunType.PISTOL: "+2 Crit damage, +3 recoil",
        GunType.SHOTGUN: "-1 ACC, +3 Recoil, +3 DMG",
        GunType.SNIPER: "+2 DMG, +4 Recoil",
        GunType.ROCKET: "+1 Crit Die, +2 Recoil",
    },
    ManufacturerNormal.MALIWAN: {
        GunType.RIFLE: "+1 Hit with Elemental Weapons",
        GunType.SUBMACHINE: "+1 ACC, +1 Elemental Damage Die",
        GunType.PISTOL: "+1 Crit damage on elemental attacks",
        GunType.SHOTGUN: "+1 ACC, +1 MST",
        GunType.SNIPER: "+1 ACC, +1 Elemental Damage Die added on crits",
        GunType.ROCKET: "+2 Accuracy, +1 SPD, -2 DMG",
    },
    ManufacturerNormal.TEDIORE: {
        GunType.RIFLE: "-2 DMG, +1 ACC",
        GunType.SUBMACHINE: "Reload on a 2 or less, +2 Accuracy, -1 DMG",
        GunType.PISTOL: "+1 Recoil",
        GunType.SHOTGUN: "Does Nothing",
        GunType.SNIPER: "+1 ACC, +3 Recoil",
        GunType.ROCKET: "Does Nothing",
    },
    ManufacturerNormal.TORGUE: {
        GunType.RIFLE: "+3 DMG, +2 Recoil, -2 ACC",
        GunType.SUBMACHINE: "-2 ACC, +2 DMG",
        GunType.PISTOL: "+2 Damage, +2 Recoil",
        GunType.SHOTGUN: "+4 DMG, +5 Recoil, -2 ACC",
        GunType.SNIPER: "+4 Recoil, -2 ACC, +3 DMG",
        GunType.ROCKET: "+4 Damage, -1 ACC, -1 SPD, +2 Recoil",
    },
    ManufacturerNormal.VLADOF: {
        GunType.RIFLE: "+2 Hits, -5 ACC, +1 Recoil",
        GunType.SUBMACHINE: "+1 Hit, +2 Recoil",
        GunType.PISTOL: "+1 Range",
        GunType.SHOTGUN: "+2 SPD, +2 Recoil",
        GunType.SNIPER: "+1 Hit, +3 Recoil",
        GunType.ROCKET: "+2 SPD, -1 ACC",
    },
}

magazine_data = {
    ManufacturerNormal.ATLAS: {
        GunType.RIFLE: "1 MST, 1 RANGE",
        GunType.SUBMACHINE: "+1 reload reroll per combat",
        GunType.PISTOL: "+1 reload reroll per combat",
        GunType.SHOTGUN: "1 ACC",
        GunType.SNIPER: "1 SPD, 1 RECOIL",
        GunType.ROCKET: "1 MST, -1 ACC",
    },
    ManufacturerNormal.COV: {
        GunType.RIFLE: "1 ACC, -1 DAMAGE",
        GunType.SUBMACHINE: "+1 Damage first attack per turn, +3 Recoil after reloading",
        GunType.PISTOL: "+1 Damage first attack per turn, +3 Recoil after reloading",
        GunType.SHOTGUN: "DOES NOTHING",
        GunType.SNIPER: "1 DMG, 1 RECOIL",
        GunType.ROCKET: "-1 ACC",
    },
    ManufacturerNormal.DAHL: {
        GunType.RIFLE: "2 ACC, -1 SPD",
        GunType.SUBMACHINE: "+1 ACC on your first attack per turn",
        GunType.PISTOL: "+1 ACC on your first attack per turn",
        GunType.SHOTGUN: "1 ACC",
        GunType.SNIPER: "-1 RECOIL, -1 ACC",
        GunType.ROCKET: "1 ACC",
    },
    ManufacturerNormal.HYPERION: {
        GunType.RIFLE: "1 ACC",
        GunType.SUBMACHINE: "+4 ACC after a reload",
        GunType.PISTOL: "+4 ACC after a reload",
        GunType.SHOTGUN: "-1 RECOIL",
        GunType.SNIPER: "2 ACC, -1 RECOIL",
        GunType.ROCKET: "1 ACC",
    },
    ManufacturerNormal.JAKOBS: {
        GunType.RIFLE: "1 ACC, 1 DAMAGE, 4 RECOIL",
        GunType.SUBMACHINE: "+1 Crit damage, Each Crit adds +1 Recoil",
        GunType.PISTOL: "+1 Crit damage, Each Crit adds +1 Recoil",
        GunType.SHOTGUN: "2 RECOIL",
        GunType.SNIPER: "2 ACC, 3 RECOIL",
        GunType.ROCKET: "2 DAMAGE, 3 RECOIL",
    },
    ManufacturerNormal.MALIWAN: {
        GunType.RIFLE: "1 MST, 1 ACC",
        GunType.SUBMACHINE: "+1 Damage on elemental damage die",
        GunType.PISTOL: "+1 Damage on elemental damage die",
        GunType.SHOTGUN: "1 ACC",
        GunType.SNIPER: "1 ACC",
        GunType.ROCKET: "2 SPD",
    },
    ManufacturerNormal.TEDIORE: {
        GunType.RIFLE: "-1 DAMAGE, -1 ACC",
        GunType.SUBMACHINE: "on tediore weapons, reload grenade damage is quadrupled",
        GunType.PISTOL: "on tediore weapons, reload grenade damage is quadrupled",
        GunType.SHOTGUN: "1 RECOIL",
        GunType.SNIPER: "1 ACC, -1 DMG",
        GunType.ROCKET: "-2 ACCURACY, -1 DMG",
    },
    ManufacturerNormal.TORGUE: {
        GunType.RIFLE: "-1 RECOIL, -1 ACC",
        GunType.SUBMACHINE: "+2 Damage per damage die on your attack after a reload",
        GunType.PISTOL: "+2 Damage per damage die on your attack after a reload",
        GunType.SHOTGUN: "2 RECOIL",
        GunType.SNIPER: "2 DMG, 2 RECOIL",
        GunType.ROCKET: "2 DAMAGE, -2 SPD",
    },
    ManufacturerNormal.VLADOF: {
        GunType.RIFLE: "2 SPD, 1 RECOIL",
        GunType.SUBMACHINE: "+1 Speed on turn when using this pistol, gives +2 recoil when using all the speed",
        GunType.PISTOL: "+1 Speed on turn when using this pistol, gives +2 recoil when using all the speed",
        GunType.SHOTGUN: "1 SPD",
        GunType.SNIPER: "1 SPD, -1 ACC",
        GunType.ROCKET: "3 SPD, 4 RECOIL",
    },
}
redtext_data = [
    {"id": 1, "name": "POP POP!", "effect": "Deals Crit Damage twice."},
    {"id": 2, "name": "I never freeze", "effect": "Adds Cryo Element type."},
    {"id": 3, "name": "Toasty!", "effect": "Adds Incendiary Element type."},
    {"id": 4, "name": "Was he slow?", "effect": "Fires backwards."},
    {
        "id": 5,
        "name": "We Hate You, Please Die.",
        "effect": "Taunts the farthest Enemy each turn.",
    },
    {
        "id": 6,
        "name": "Tell them they're next",
        "effect": "Won't deal Damage to the final Enemy in an encounter.",
    },
    {"id": 7, "name": "PAN SHOT!", "effect": "Always Hits the closest Enemy."},
    {"id": 8, "name": "Envision Wyverns", "effect": "Adds Radiation Element type."},
    {"id": 9, "name": "I'm melting!", "effect": "Adds Corrosive Element type."},
    {
        "id": 10,
        "name": "The same thing that happens to everything else.",
        "effect": "Adds Shock Element type.",
    },
    {
        "id": 11,
        "name": "360 quickscope",
        "effect": "Adds a Crit to each Ranged Attack.",
    },
    {
        "id": 12,
        "name": "Any Questions?",
        "effect": "Shoots pumpkin bombs that deal an extra 3d6 Explosive Damage.",
    },
    {
        "id": 13,
        "name": "Blood and Thunder",
        "effect": "Take 1d6 Health Damage to deal +3d6 Shock Damage.",
    },
    {
        "id": 14,
        "name": "SI VIS PACEM, PARA BELLUM",
        "effect": "Gain Extra Attack if Acting Before Enemies.",
    },
    {
        "id": 15,
        "name": "You're breathtaking!",
        "effect": "Wielder cannot be targeted on the first turn of an encounter.",
    },
    {
        "id": 16,
        "name": "Pass turn.",
        "effect": "Wielder may Throw a grenade during the End of Turn step.",
    },
    {
        "id": 17,
        "name": "I am Vengeance!",
        "effect": "Deals 2x Damage to Enemies adjacent to allies.",
    },
    {
        "id": 18,
        "name": "Roll the dice",
        "effect": "If Accuracy Roll is even, 2x Damage. If Accuracy Roll is odd, half Damage.",
    },
    {
        "id": 19,
        "name": "One among the fence",
        "effect": "Add 21 Damage if you roll 13+ on your Accuracy Roll. (1/day)",
    },
    {
        "id": 20,
        "name": "Don't be sorry. Be better.",
        "effect": "Reroll the Badass Die once per day.",
    },
    {
        "id": 21,
        "name": "THE PICKLES!",
        "effect": "Shoots flaming cheeseburgers that deal an extra 2d6 Incendiary Damage.",
    },
    {
        "id": 22,
        "name": "Do a kickflip!",
        "effect": "+4 on Traverse Checks while equipped.",
    },
    {
        "id": 23,
        "name": "Extinction is the Rule",
        "effect": "Teleport to any square up to 4 away when you kill an Enemy.",
    },
    {
        "id": 24,
        "name": "Never Fight a Knight with a Perm",
        "effect": "DMG Mod +6 against non-human Enemies.",
    },
    {
        "id": 25,
        "name": "Bye bye, little Butt Stallion!",
        "effect": "Shots explode into rainbows that deal an extra 1d8 Damage.",
    },
    {
        "id": 26,
        "name": "Time 2 Hack",
        "effect": "+4 on Interact Checks and Melee Damage while equipped.",
    },
    {
        "id": 27,
        "name": "HATE Magic...",
        "effect": "so much +3 DMG Mod. Take 2d6 Vomit Damage if Reloaded.",
    },
    {
        "id": 28,
        "name": "OFF WITH THEIR HEADS!",
        "effect": "Roll %s. 95%+: the Enemy's head falls off.",
    },
    {
        "id": 29,
        "name": "This is my BOOMSTICK!",
        "effect": "Deals 3x Damage to skeletons.",
    },
    {
        "id": 30,
        "name": "Super easy, barely an inconvenience",
        "effect": "Automatically pass the first Check each day.",
    },
    {
        "id": 31,
        "name": "Hold onto your butts.",
        "effect": "When fired, the wielder and targets Hit are Knocked Back 2 squares.",
    },
    {
        "id": 32,
        "name": "The Wise Man's Fear",
        "effect": "Deals 3x Damage to all wizards.",
    },
    {
        "id": 33,
        "name": "I don't want this isolation.",
        "effect": "Won't fire unless adjacent to an ally or target.",
    },
    {
        "id": 34,
        "name": "TUFF with two Fs",
        "effect": "Prevents the first 5 Health Damage each turn.",
    },
    {
        "id": 35,
        "name": "Unlikely Maths",
        "effect": "Roll an extra die of each type rolled during an Attack and take the highest result(s).",
    },
    {
        "id": 36,
        "name": "Gravity's Rainbow",
        "effect": "First Attack against a Badass target always deals max Damage.",
    },
    {
        "id": 37,
        "name": "Let's do this one last time...",
        "effect": "Shoots webs that reduce target's Movement to 0 for 1 turn.",
    },
    {
        "id": 38,
        "name": "BIP!",
        "effect": "Once per encounter, the wielder can run into squares with an Enemy, Knocking them Back 1 square.",
    },
    {
        "id": 39,
        "name": "The Heaviest Matter of the Universe",
        "effect": "The wielder and targets Hit cannot take Movement Actions while equipped.",
    },
    {
        "id": 40,
        "name": "GREEN FLAME",
        "effect": "Shoots burst of green flames while firing, dealing 2d6 Incendiary Damage to adjacent targets.",
    },
    {
        "id": 41,
        "name": "More like Bore Ragnarok!",
        "effect": "Gain 1 Badass Token after a successful Talk Check while equipped.",
    },
    {
        "id": 42,
        "name": "That's levitation, Holmes!",
        "effect": "Ignore difficult terrain while equipped.",
    },
    {
        "id": 43,
        "name": "Let's boo-boo.",
        "effect": "Gain Extra Movement after drinking a potion while equipped.",
    },
    {
        "id": 44,
        "name": "Mmm Whatcha Say...",
        "effect": "Gain a Ranged Attack if an Enemy is talking before an encounter.",
    },
    {
        "id": 45,
        "name": "Here Comes the FunCooker",
        "effect": "When this gun scores a Crit, the Enemy suffers a miniature combustion, dealing 1d12 Explosive Damage to itself and all adjacent squares.",
    },
    {
        "id": 46,
        "name": "Overwhelming strength is boring.",
        "effect": "\u00e2\u20ac\u201c6 Initiative. The first non-Badass, non- boss Enemy that is Melee Attacked dies instantly (1/day).",
    },
    {
        "id": 47,
        "name": "Stop talking, I will win.",
        "effect": "It's what heroes do. Gun fires explosives that deal +3d6 Damage to all adjacent squares.",
    },
    {
        "id": 48,
        "name": "Richer and cleverer than everyone else!",
        "effect": "Add 10 gold per Loot Pile when rolling for Enemy Drops.",
    },
    {
        "id": 49,
        "name": "METAL WILL DESTROY ALL EVIL!",
        "effect": "Allies get +2 ACC Mod each turn you perform a Melee Attack.",
    },
    {
        "id": 50,
        "name": "Life is a conundrum of esoterica.",
        "effect": "Gain 2 Badass Tokens the first time you roll for a Trauma each day.",
    },
]

prefix_data = [
    {
        "name": "Loaded",
        "normal": "+1 reload reroll / combat",
        "affinity": ManufacturerNormal.ATLAS,
        "boosted": "2 reload reroll / combat",
    },
    {
        "name": "Stabbing",
        "normal": "gun damage die added on melee attack",
        "affinity": ManufacturerNormal.COV,
        "boosted": "gun damage die added on melee attack",
    },
    {
        "name": "Tactical",
        "normal": "-1 recoil",
        "affinity": ManufacturerNormal.DAHL,
        "boosted": "-2 recoil",
    },
    {
        "name": "Earnest",
        "normal": "+1 ACC",
        "affinity": ManufacturerNormal.HYPERION,
        "boosted": "+2 ACC",
    },
    {
        "name": "Deadly",
        "normal": "+1 Crit Damage",
        "affinity": ManufacturerNormal.JAKOBS,
        "boosted": "+2 Crit Damage",
    },
    {
        "name": "Bewitching",
        "normal": "+1 Damage on elemental rolls",
        "affinity": ManufacturerNormal.MALIWAN,
        "boosted": "+2 Damage on elemental rolls",
    },
    {
        "name": "Expendable",
        "normal": "reload on a roll of 2 or less",
        "affinity": ManufacturerNormal.TEDIORE,
        "boosted": "reload on a roll of 5 or less",
    },
    {
        "name": "Double Penetrating",
        "normal": "+5 recoil, +1 hit",
        "affinity": ManufacturerNormal.TORGUE,
        "boosted": "+4 recoil, +2 hit",
    },
    {
        "name": "Vengeful",
        "normal": "+1 hit on 16+ACC",
        "affinity": ManufacturerNormal.VLADOF,
        "boosted": "+2 hits on 16+ACC",
    },
]


boost_gripmanufacturermatch = "-1 Recoil on all attacks, once per encounter you can reroll an accuracy roll with this weapon"


@router.post("/generate")
def roll_gun(create_result: random_create_result, session: SessionDep) -> roll_response:
    print(create_result)
    # PART 1 gun roll
    gunroll = create_result.get_roll_for_label("Gun roll")

    # get guntype
    guntypeint = gunmask[gunroll[0] - 1][gunroll[0] - 1]
    if guntypeint == -1:
        temp = create_result.get_selection_for_label("favoured_guns")
        if len(temp) == 0:
            temp = [member.value for member in GunType]
        guntype = GunType(random.choice(temp))
    else:
        guntype = GunTypeIndexed[guntypeint]

    guntype_choice = create_result.get_option_for_label("enforce_guntype")
    if not (guntype_choice == None or len(guntype_choice) == 0):
        guntype = GunType(guntype_choice[0])

    # get manufacturer
    manufacturerint = manufacturerMask[gunroll[0] - 1][gunroll[0] - 1]
    if manufacturerint == -1:
        temp = create_result.get_selection_for_label("favoured_manufacturer")
        if len(temp) == 0:
            temp = [member.value for member in Manufacturer]
        manufacturer = Manufacturer(random.choice(temp))
    else:
        manufacturer = ManufacturerIndexed[manufacturerint]

    manufacturer_choice = create_result.get_option_for_label("enforce_manufacturer")
    if not (manufacturer_choice == None or len(manufacturer_choice) == 0):
        manufacturer = Manufacturer(manufacturer_choice[0])
        manufacturer_normal = ManufacturerMappedToNormal[manufacturer]

    # PART 2 rarity (hmm dat was makkelijk)
    rarityRoll = create_result.get_roll_for_label("Rarity roll")
    rarity = RarityIndexed[rarityMask[rarityRoll[0] - 1][rarityRoll[1] - 1]]

    rarity_choice = create_result.get_option_for_label("rarity")
    if not (rarity_choice == None or len(rarity_choice) == 0):
        rarity = Rarity(rarity_choice[0])

    # PART 3 element
    hasElement = elementalRolMask[rarityRoll[0] - 1][rarityRoll[1] - 1]
    if guildElementalOverrideMask[manufacturer] == -1:
        hasElement = False
    if guildElementalOverrideMask[manufacturer] == 1:
        hasElement = True
    elyroll = 0
    if hasElement:
        elyroll = create_result.get_roll_for_label("Element roll")[0]
        if manufacturer == Manufacturer.MALEFACTOR:
            match rarity:
                case Rarity.LEGENDARY:
                    elyroll += 20
                case Rarity.EPIC:
                    elyroll += 15
                case Rarity.RARE:
                    elyroll += 10
                case _:
                    pass
        if elyroll > 100:
            elyroll = 100
    # TODO refactor deze map, of steek het tenminste in ne file
    # => nope grote maps in de files is nu standaard
    element = None
    elementstr = ""
    for row in 5:
        if row["range"][0] <= elyroll and row["range"][1] >= elyroll:
            element = row["rarity"][rarity][0]
            elementstr = row["rarity"][rarity][1]
            break

    # PART4 prefix
    # d20 => 1-11 nothing, 12-20 has prefix
    prefix_name = ""
    prefix_effect = ""
    prefixRoll = create_result.get_roll_for_label("Prefix")[0]
    if prefixRoll > 11:
        prefix = prefix_data[prefixRoll - 11]
        prefix_name = prefix["name"]
        prefix_effect = prefix["normal"]
        if prefix["affinity"] == manufacturer_normal:
            prefix_effect = prefix["boosted"]

    # PART5 redtext
    redtext_name = ""
    redtext_effect = ""
    if rarity in [Rarity.EPIC, Rarity.LEGENDARY]:
        redtextRoll = create_result.get_roll_for_label("Redtext")[0]
        redtext = redtext_data[int(redtextRoll / 2)]
        redtext_name = redtext["name"]
        redtext_effect = redtext["effect"]

    # PART6 damage numbers
    damagerow = None
    for row in damageMap[guntype]:
        if row[0][0] <= create_result.level and row[0][1] >= create_result.level:
            damagerow = row[1]
            break

    # PART7 parts
    parts_roll = (
        create_result.get_roll_for_label("Parts")[0]
        * create_result.get_roll_for_label("Parts")[1]
    ) + create_result.get_roll_for_label("Parts")[2]
    # decode single number into 3 numbers from 1-9
    sum_value = 3 + int((parts_roll - 1) * 24 / 1999)
    base = sum_value // 3
    remainder = sum_value % 3
    digits = [base] * 3
    for i in range(remainder):
        digits[i] += 1
    for i in range(3):
        if digits[i] < 1:
            digits[i] = 1
        elif digits[i] > 9:
            digits[i] = 9

    barrel_roll = digits[0]
    magazine_roll = digits[1]
    grip_roll = digits[2]

    legun = GunCreate(
        name="nog niets",
        description="ook nog niets",
        rarity=rarity,
        guntype=guntype,
        manufacturer=manufacturer,
        manufacturer_effect=guildRarityBonusMap[manufacturer][rarity],
        element=element,
        elementstr=elementstr,
        prefix_ids=prefix,
        postfix_ids=[],
        redtext_ids=redtext,
        range=gunRangeMap[guntype],
        dmgroll=damagerow[1],
        lowNormal=damagerow[0][0],
        lowCrit=damagerow[0][1],
        mediumNormal=damagerow[0][2],
        mediumCrit=damagerow[0][3],
        highNormal=damagerow[0][4],
        highCrit=damagerow[0][5],
    )
    gotten_gun = create_gun(gun_data=legun, session=session)
    return roll_response(item_id=gotten_gun.id, item_type="gun")


@router.get("/{gun_id}", response_model=GunResponse)
def get_gun(gun_id: str, session: SessionDep) -> GunResponse:
    statement = (
        select(Gun)
        .options(selectinload(Gun.prefixes), selectinload(Gun.postfixes))
        .where(Gun.id == gun_id)
    )

    gun = session.exec(statement).first()

    if gun is None:
        raise HTTPException(status_code=404, detail="Gun not found")
    # Yup de sqlmodel naar pydantic werkt niet met foreig n eky object expansio
    temp = Gun.model_dump(gun)
    temp["prefixes"] = gun.prefixes
    temp["postfixes"] = gun.postfixes
    temp["redtexts"] = gun.redtexts

    return GunResponse.model_validate(temp)


@router.post("/")
def create_gun(gun_data: GunCreate, session: SessionDep) -> Gun:
    # Create a new Gun instance
    gun = Gun(
        id=str(uuid.uuid4()),
        type=gun_data.guntype,
        name=gun_data.name,
        description=gun_data.description,
        rarity=gun_data.rarity,
        manufacturer=gun_data.manufacturer,
        manufacturer_effect=gun_data.manufacturer_effect,
        element=gun_data.element,
        elementstr=gun_data.elementstr,
        range=gun_data.range,
        dmgroll=gun_data.dmgroll,
        lowNormal=gun_data.lowNormal,
        lowCrit=gun_data.lowCrit,
        mediumNormal=gun_data.mediumNormal,
        mediumCrit=gun_data.mediumCrit,
        highNormal=gun_data.highNormal,
        highCrit=gun_data.highCrit,
    )

    session.add(gun)
    histoir = RollHistory(
        id=gun.id, date=datetime.now(), description=str(gun), type="Gun"
    )
    session.add(histoir)
    session.commit()
    session.refresh(gun)

    for prefix_id in gun_data.prefix_ids:
        prefix = session.get(Prefix, prefix_id)
        if prefix:
            gun.prefixes.append(prefix)
        else:
            raise HTTPException(
                status_code=404, detail=f"Prefix with id {prefix_id} not found"
            )

    for postfix_id in gun_data.postfix_ids:
        postfix = session.get(Postfix, postfix_id)
        if postfix:
            gun.postfixes.append(postfix)
        else:
            raise HTTPException(
                status_code=404, detail=f"Postfix with id {postfix_id} not found"
            )

    for redtext_id in gun_data.redtext_ids:
        redtext = session.get(RedText, redtext_id)
        if redtext:
            gun.redtexts.append(redtext)
        else:
            raise HTTPException(
                status_code=404, detail=f"Redtext with id {redtext_id} not found"
            )

    session.commit()
    session.refresh(gun)

    return gun


@router.put("/{gun_id}", response_model=GunResponse)
def update_gun(gun_id: str, gun: GunResponse, session: SessionDep) -> GunResponse:
    statement = select(Gun).where(Gun.id == gun_id)
    results = session.exec(statement)
    gun_db = results.one()
    gun_db.id = gun.id
    gun_db.name = gun.name
    gun_db.description = gun.description
    gun_db.type = gun.type
    gun_db.rarity = gun.rarity
    gun_db.manufacturer = gun.manufacturer
    gun_db.manufacturer_effect = gun.manufacturer_effect
    gun_db.element = gun.element
    gun_db.elementstr = gun.elementstr
    gun_db.range = gun.range
    gun_db.dmgroll = gun.dmgroll
    gun_db.lowNormal = gun.lowNormal
    gun_db.lowCrit = gun.lowCrit
    gun_db.mediumNormal = gun.mediumNormal
    gun_db.mediumCrit = gun.mediumCrit
    gun_db.highNormal = gun.highNormal
    gun_db.highCrit = gun.highCrit

    session.add(gun_db)
    session.commit()
    session.refresh(gun_db)
    return gun_db
