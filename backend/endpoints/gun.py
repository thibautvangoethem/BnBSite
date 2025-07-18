from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
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
                roll_description(label="Prefix", diceList=[Dice.D100]),
                roll_description(label="Redtext", diceList=[Dice.D100]),
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
    element = None
    elementstr = ""
    for row in elementalRarityRolArray:
        if row["range"][0] <= elyroll and row["range"][1] >= elyroll:
            element = row["rarity"][rarity][0]
            elementstr = row["rarity"][rarity][1]
            break

    # PART4 prefix
    if rarity in [Rarity.RARE, Rarity.EPIC, Rarity.LEGENDARY]:
        prefixRoll = create_result.get_roll_for_label("Prefix")[0]
        prefix = [prefixRoll]
    else:
        prefix = []

    # PART5 redtext
    if rarity in [Rarity.EPIC, Rarity.LEGENDARY]:
        redtextRoll = create_result.get_roll_for_label("Redtext")[0]
        redtext = [int(redtextRoll / 2)]
    else:
        redtext = []

    # PART6 damage numbers
    damagerow = None
    for row in damageMap[guntype]:
        if row[0][0] <= create_result.level and row[0][1] >= create_result.level:
            damagerow = row[1]
            break

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
