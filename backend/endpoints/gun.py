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
class GunCreate(SQLModel):
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
    lowNormal: int
    lowCrit: int
    mediumNormal: int
    mediumCrit: int
    highNormal: int
    highCrit: int


@router.get("/")
def read_guns(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Gun]:
    guns = session.exec(select(Gun).offset(offset).limit(limit)).all()
    return guns


@router.get("/rolldescription", response_model=random_create_description)
def get_create_descritpion(session: SessionDep) -> random_create_description:
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
            optional=[],  # todo optional choice later
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
    [
        [1, 10],
        [
            [Element.NIETS, "Klaag bij Thibaut, dit kunde nie eens rollen"],
            [Element.NIETS, "Klaag bij Thibaut, dit kunde nie eens rollen"],
            [Element.NIETS, "Klaag bij Thibaut, dit kunde nie eens rollen"],
            [Element.NIETS, "Klaag bij Thibaut, dit kunde nie eens rollen"],
            [Element.NIETS, "Klaag bij Thibaut, dit kunde nie eens rollen"],
        ],
    ],
    [
        [11, 15],
        [
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.RADIATION, "Radiation"],
            [Element.RADIATION, "Radiation"],
        ],
    ],
    [
        [16, 20],
        [
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.CORROSIVE, "Corrosive"],
            [Element.CORROSIVE, "Corrosive"],
        ],
    ],
    [
        [21, 25],
        [
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.SHOCK, "Shock"],
            [Element.SHOCK, "Shock"],
        ],
    ],
    [
        [26, 30],
        [
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.RADIATION, "Radiation"],
            [Element.EXPLOSIVE, "Explosive"],
            [Element.EXPLOSIVE, "Explosive"],
        ],
    ],
    [
        [31, 35],
        [
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.CORROSIVE, "Corrosive"],
            [Element.INCENDIARY, "Incendiary"],
            [Element.INCENDIARY, "Incendiary"],
        ],
    ],
    [
        [36, 40],
        [
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.SHOCK, "Shock"],
            [Element.CRYO, "Cryo"],
            [Element.CRYO, "Cryo"],
        ],
    ],
    [
        [41, 45],
        [
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.EXPLOSIVE, "Explosive"],
            [Element.RADIATION, "Radiation (+1d6)"],
            [Element.RADIATION, "Radiation (+1d6)"],
        ],
    ],
    [
        [46, 50],
        [
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.INCENDIARY, "Incendiary"],
            [Element.CORROSIVE, "Corrosive (+1d6)"],
            [Element.CORROSIVE, "Corrosive (+1d6)"],
        ],
    ],
    [
        [51, 55],
        [
            [Element.NIETS, "N/A"],
            [Element.NIETS, "N/A"],
            [Element.CRYO, "Cryo"],
            [Element.SHOCK, "Shock (+1d6)"],
            [Element.SHOCK, "Shock (+1d6)"],
        ],
    ],
    [
        [56, 60],
        [
            [
                Element.NIETS,
                "N/A",
            ],
            [
                Element.RADIATION,
                "Radiation",
            ],
            [
                Element.RADIATION,
                "Radiation (+1d6)",
            ],
            [
                Element.EXPLOSIVE,
                "Explosive (+1d6)",
            ],
            [
                Element.EXPLOSIVE,
                "Explosive (+1d6)",
            ],
        ],
    ],
    [
        [61, 65],
        [
            [
                Element.NIETS,
                "N/A",
            ],
            [
                Element.CORROSIVE,
                "Corrosive",
            ],
            [
                Element.CORROSIVE,
                "Corrosive (+1d6)",
            ],
            [
                Element.INCENDIARY,
                "Incendiary (+1d6)",
            ],
            [
                Element.INCENDIARY,
                "Incendiary (+1d6)",
            ],
        ],
    ],
    [
        [66, 70],
        [
            [Element.NIETS, "N/A"],
            [Element.SHOCK, "Shock"],
            [Element.SHOCK, "Shock (+1d6)"],
            [Element.CRYO, "Cryo (+1d6)"],
            [Element.CRYO, "Cryo (+1d6)"],
        ],
    ],
    [
        [71, 75],
        [
            [
                Element.NIETS,
                "N/A",
            ],
            [
                Element.EXPLOSIVE,
                "Explosive",
            ],
            [
                Element.EXPLOSIVE,
                "Explosive (+1d6)",
            ],
            [
                Element.RADIATION,
                "Radiation (+2d6)",
            ],
            [
                Element.RADIATION,
                "Radiation (+2d6)",
            ],
        ],
    ],
    [
        [76, 80],
        [
            [
                Element.NIETS,
                "N/A",
            ],
            [
                Element.INCENDIARY,
                "Incendiary",
            ],
            [
                Element.INCENDIARY,
                "Incendiary (+1d6)",
            ],
            [
                Element.CORROSIVE,
                "Corrosive (+2d6)",
            ],
            [
                Element.CORROSIVE,
                "Corrosive (+2d6)",
            ],
        ],
    ],
    [
        [81, 85],
        [
            [Element.NIETS, "N/A"],
            [Element.CRYO, "Cryo"],
            [Element.CRYO, "Cryo (+1d6)"],
            [Element.SHOCK, "Shock (+2d6)"],
            [Element.SHOCK, "Shock (+2d6)"],
        ],
    ],
    [
        [86, 90],
        [
            [
                Element.RADIATION,
                "Radiation",
            ],
            [
                Element.RADIATION,
                "Radiation (+1d6)",
            ],
            [
                Element.RADIATION,
                "Radiation (+2d6)",
            ],
            [
                Element.EXPLOSIVE,
                "Explosive (+2d6)",
            ],
            [
                Element.EXPLOSIVE,
                "Explosive (+2d6)",
            ],
        ],
    ],
    [
        [91, 92],
        [
            [
                Element.CORROSIVE,
                "Corrosive",
            ],
            [
                Element.CORROSIVE,
                "Corrosive (+1d6)",
            ],
            [
                Element.CORROSIVE,
                "Corrosive (+2d6)",
            ],
            [
                Element.INCENDIARY,
                "Incendiary (+2d6)",
            ],
            [
                Element.INCENDIARY,
                "Incendiary (+2d6)",
            ],
        ],
    ],
    [
        [93, 94],
        [
            [Element.SHOCK, "Shock"],
            [Element.SHOCK, "Shock (+1d6)"],
            [Element.SHOCK, "Shock (+2d6)"],
            [Element.CRYO, "Cryo (+2d6)"],
            [Element.CRYO, "Cryo (+2d6)"],
        ],
    ],
    [
        [95, 96],
        [
            [
                Element.EXPLOSIVE,
                "Explosive",
            ],
            [
                Element.EXPLOSIVE,
                "Explosive (+1d6)",
            ],
            [
                Element.EXPLOSIVE,
                "Explosive (+2d6)",
            ],
            [
                Element.OEPS,
                "Radiation + Incendiary",
            ],
            [
                Element.OEPS,
                "Radiation + Incendiary",
            ],
        ],
    ],
    [
        [97, 98],
        [
            [
                Element.INCENDIARY,
                "Incendiary",
            ],
            [
                Element.INCENDIARY,
                "Incendiary (+1d6)",
            ],
            [
                Element.INCENDIARY,
                "Incendiary (+2d6)",
            ],
            [
                Element.OEPS,
                "Shock + Corrosive",
            ],
            [
                Element.OEPS,
                "Shock + Corrosive",
            ],
        ],
    ],
    [
        [99, 100],
        [
            [Element.CRYO, "Cryo"],
            [Element.CRYO, "Cryo (+1d6)"],
            [Element.CRYO, "Cryo (+2d6)"],
            [Element.OEPS, "Explosive + Cryo"],
            [Element.OEPS, "Explosive + Cryo"],
        ],
    ],
]


@router.post("/generate")
def roll_gun(create_result: random_create_result, session: SessionDep) -> roll_response:
    print(create_result)
    # PART 1 gun roll
    gunroll = create_result.get_roll_for_label("Gun roll")

    # get guntype
    guntypeint = gunmask[gunroll[0] - 1][gunroll[0] - 1]
    if guntypeint == -1:
        guntype = GunType(
            random.choice(create_result.get_selection_for_label("favoured_guns"))
        )
    else:
        guntype = GunTypeIndexed[guntypeint]

    # get manufacturer
    manufacturerint = manufacturerMask[gunroll[0] - 1][gunroll[0] - 1]
    if manufacturerint == -1:
        manufacturer = Manufacturer(
            random.choice(
                create_result.get_selection_for_label("favoured_manufacturer")
            )
        )
    else:
        manufacturer = ManufacturerIndexed[manufacturerint]

    # PART 2 rarity (hmm dat was makkelijk)
    rarityRoll = create_result.get_roll_for_label("Rarity roll")
    # TODO get rid of rarint, sitll used for big element map
    rarint = rarityMask[rarityRoll[0] - 1][rarityRoll[1] - 1]
    rarity = RarityIndexed[rarityMask[rarityRoll[0] - 1][rarityRoll[1] - 1]]

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
        if row[0][0] <= elyroll and row[0][1] >= elyroll:
            element = row[1][rarint][0]
            elementstr = row[1][rarint][1]
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
        range=-100,
        lowNormal=-100,
        lowCrit=-100,
        mediumNormal=-100,
        mediumCrit=-100,
        highNormal=-100,
        highCrit=-100,
    )
    gotten_gun = create_gun(gun_data=legun, session=session)
    return roll_response(item_id=gotten_gun.id, item_type="gun")


@router.get("/{gun_id}", response_model=Gun)
def get_gun(gun_id: str, session: SessionDep) -> Prefix:
    statement = (
        select(Gun)
        .options(selectinload(Gun.prefixes), selectinload(Gun.postfixes))
        .where(Gun.id == gun_id)
    )

    gun = session.exec(statement).first()

    if gun is None:
        raise HTTPException(status_code=404, detail="Gun not found")

    return gun


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
