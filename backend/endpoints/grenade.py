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
from models.grenade import Grenade


import uuid

router = APIRouter(
    prefix="/grenades",
    tags=["grenade"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/rolldescription", response_model=random_create_description)
def get_create_descritpion(session: SessionDep) -> random_create_description:
    description = random_create_description(
        level=True,
        selections=selection_descriptions(
            mandatory=[],
            optional=[],  # todo optional choice later
        ),
        rolls=rollswrapper(
            entries=[
                roll_description(label="Rarity roll", diceList=[Dice.D100]),
                roll_description(label="Manufacturer", diceList=[Dice.D8]),
                roll_description(label="Grenade primer", diceList=[Dice.D8]),
                roll_description(label="detonator", diceList=[Dice.D8]),
                roll_description(label="Redtext", diceList=[Dice.D10]),
            ],
            uuid=str(uuid4()),
        ),
    )
    return description


@router.get("/{grenade_id}", response_model=Grenade)
def get_grenade(grenade_id: str, session: SessionDep) -> Grenade:
    statement = select(Grenade).where(Grenade.id == grenade_id)

    grenade = session.exec(statement).first()

    if grenade is None:
        raise HTTPException(status_code=404, detail="grenade not found")

    return grenade


roll_rarity = [
    ((1, 40), Rarity.COMMON),
    ((41, 70), Rarity.UNCOMMON),
    ((71, 85), Rarity.RARE),
    ((86, 95), Rarity.EPIC),
    ((96, 100), Rarity.LEGENDARY),
]

manufacturer_data = {
    Manufacturer.DAHLIA: {
        Rarity.COMMON: "Can be thrown 2 tiles further, does 75% damage.",
        Rarity.UNCOMMON: "Can be thrown 3 tiles further, does 85% damage.",
        Rarity.RARE: "Can be thrown 4 tiles further, does 95% damage.",
        Rarity.EPIC: "Can be thrown 5 tiles further, does 105% damage. +1 square radius",
        Rarity.LEGENDARY: "Can be thrown 6 tiles further, does 120% damage. +1 square radius",
    },
    Manufacturer.FERIORE: {
        Rarity.COMMON: "no change",
        Rarity.UNCOMMON: "+10% damage",
        Rarity.RARE: "+20% damage",
        Rarity.EPIC: "+30% damage",
        Rarity.LEGENDARY: "+40% damage, releases 3 smaller explosions on the target dealing half damage each",
    },
    Manufacturer.MALEFACTOR: {
        Rarity.COMMON: "-10% damage",
        Rarity.UNCOMMON: "no change",
        Rarity.RARE: "+10% damage, +1 square radius",
        Rarity.EPIC: "+20% damage, +1 square radius",
        Rarity.LEGENDARY: "+40% damage, +2 square radius, leaves a lingering matching element puddle for 2 turns, dealing half grenade damage for EVERYTHING standing inside it",
    },
    Manufacturer.TORGUE: {
        Rarity.COMMON: "+25% DAMAGE, -1 grenade capacity while equipped",
        Rarity.UNCOMMON: "+40% DAMAGE, -1 grenade capacity while equipped",
        Rarity.RARE: "+55% DAMAGE, -1 grenade capacity while equipped, +1 square radius",
        Rarity.EPIC: "+75% DAMAGE, -1 grenade capacity while equipped, +1 square radius",
        Rarity.LEGENDARY: "+100% DAMAGE, -1 grenade capacity while equipped, double radius",
    },
    Manufacturer.HYPERIUS: {
        Rarity.COMMON: "-25% damage, -1 square radius",
        Rarity.UNCOMMON: "-10% damage",
        Rarity.RARE: "no change",
        Rarity.EPIC: "+10% damage, +1 square radius",
        Rarity.LEGENDARY: "+20% damage, +1 square radius, creates a shockwave during the explosion that staggers enemies, -2 to each damage die on their next turn.",
    },
    Manufacturer.BLACKPOWDER: {
        Rarity.COMMON: "+50% damage, -1 throw range",
        Rarity.UNCOMMON: "+65% damage, -1 throw range",
        Rarity.RARE: "+80% damage, -2 throw range, +1 square radius",
        Rarity.EPIC: "+100% damage, -2 throw range, +1 square radius",
        Rarity.LEGENDARY: "+150% damage, -3 throw range, +2 square radius, does double damage on shields, including players",
    },
    Manufacturer.STOKER: {
        Rarity.COMMON: "-70% damage, slags enemies hit, (take double damage next time they take damage)",
        Rarity.UNCOMMON: "-50% damage, slags enemies hit, (take double damage next time they take damage)",
        Rarity.RARE: "-20% damage, spawns a slag puddle for 2 turns, everyone inside takes double damage for the duration",
        Rarity.EPIC: "+1 square radius, spawns a slag puddle for 2 turns, everyone inside takes double damage for the duration",
        Rarity.LEGENDARY: "slag storm, +4 square radius, for the next 5 turns a slag storm covers the area of effect, making everyone inside take double damage from all sources",
    },
    Manufacturer.ALAS: {
        Rarity.COMMON: "+100% damage, -2 square radius",
        Rarity.UNCOMMON: "-200% damage, -2 square radius",
        Rarity.RARE: "+250% damage, -2 square radius, explodes on impact, dealing half the damage again in a 3x3 radius.",
        Rarity.EPIC: "+300% damage, -2 square radius, explodes on impact, dealing half the damage again in a 3x3 radius.",
        Rarity.LEGENDARY: "+400% damage, -2 square radius, explodes on impact, dealing half the damage again in a 3x3 radius. if any of the two effects kills, refund the grenade",
    },
}

primer_data = {
    Manufacturer.TORGUE: "+1x1 radius, -1 tile throw range",
    Manufacturer.MALEFACTOR: "grenades explode 1 turn later, +20% damage",
    Manufacturer.DAHLIA: "-10% damage, +1 range",
    Manufacturer.STOKER: "+1 square range",
    Manufacturer.BLACKPOWDER: "grenades can CRIT, (if one of the damage die thrown is max damage) dealing +50% extra total damage, -1x1 radius",
    Manufacturer.ALAS: "50% chance to spawn a second grenade on detonation, -10% base damage",
    Manufacturer.HYPERIUS: "grenades detonates twice, second explosion does 25% off the first effect",
    Manufacturer.FERIORE: "-25% less damage, but heals allies in the radius",
    Manufacturer.SKULLDUGGER: "oeps niets",
}

detonator_data = {
    Manufacturer.TORGUE: "+10% damage, -1 throw range",
    Manufacturer.MALEFACTOR: "+15% elemental damage, -10% base damage",
    Manufacturer.DAHLIA: "+2 tile throw range, -5% base damage",
    Manufacturer.STOKER: "grenade splits in two, dealing half the effect on two targets",
    Manufacturer.BLACKPOWDER: "+15% base damage, -1 grenade capacity",
    Manufacturer.ALAS: "adds one damage die from the grenade to your melee damage",
    Manufacturer.HYPERIUS: "+1 tile throw range, if applicable, grenades stick to enemies",
    Manufacturer.FERIORE: "heals for 20% of damage dealt, -10% base damage",
    Manufacturer.SKULLDUGGER: "oeps niets",
}

redtext = [
    (
        "Fearsome Repercussions",
        "Grenade explodes into a cloud of corrosive gas, dealing 50% of the grenade’s base damage over 3 turns to enemies in a 5-meter radius. Enemies that die while affected explode in a burst of corrosive damage, dealing 25% of the grenade’s base damage.",
    ),
    (
        "Silent Rebirth",
        "When this grenade explodes, all enemies within range are silenced for 2 turns, unable to use abilities that require speaking or vocalizing. Allies can still taunt enemies with silence-inducing phrases. The explosion deals 75% of the grenade’s base damage.",
    ),
    (
        "Resonating Echo",
        "Upon detonation, this grenade emits a shockwave that knocks back all nearby enemies. The shockwave deals 100% of the grenade’s base damage and has a 50% chance to interrupt any ongoing abilities. If the shockwave hits a wall, it ricochets and deals an additional 25% of the base damage to all enemies in its path.",
    ),
    (
        "Fractured Judgment",
        "Enemies hit by the explosion are critically injured, causing them to lose half of their armor and take 10% more damage from all sources for 2 turns.",
    ),
    (
        "Resonant Vortex",
        "This grenade creates a gravitational vortex, pulling enemies toward its center. Each enemy caught within 3 meters of the explosion takes 50% of the grenade’s base damage per turn they remain in the vortex for up to 2 turns.",
    ),
    (
        "Liquid Inferno",
        "Enemies within the radius are ignited, taking 30% of the grenade’s base damage each turn for 3 turns. If they’re already on fire, the grenade causes the fire to spread to other enemies within a 5-meter radius, chaining for 15% of the base damage per enemy.",
    ),
    (
        "Gravity’s End",
        "This grenade manipulates gravity, causing enemies in the blast radius to be launched into the air. The explosion deals 100% of the grenade’s base damage and causes fall damage of 50% of the base damage. If they hit a wall during the fall, they take an additional 25% of the base damage.",
    ),
    (
        "Shocking Aftermath",
        "The grenade explodes with an electric surge, chaining lightning damage to nearby enemies. Each additional enemy hit increases the damage by 10%, starting at 50% of the grenade’s base damage for the first enemy.",
    ),
    (
        "Tooth and Claw",
        "Upon detonation, the grenade releases multiple shrapnel spikes that ricochet between enemies within a 3-meter radius. Each spike deals 25% of the grenade’s base damage and has a chance to cause an additional debuff (e.g., poison, shock, or fire).",
    ),
    (
        "Chaotic Reverberation",
        "When thrown, this grenade causes all nearby weapons to misfire for 1 turn. The explosion deals 75% of the grenade’s base damage and causes wild recoil, lowering the affected enemies’ accuracy by 30% for 1 turn.",
    ),
]

level_data = [
    (1, ("1d8", "3x3")),
    (7, ("2d10", "3x3")),
    (13, ("3d12", "3x3")),
    (19, ("4d12", "3x3")),
    (25, ("6d12", "3x3")),
    (31, ("8d12", "3x3")),
    (37, ("6d20", "3x3")),
    (43, ("8d20", "3x3")),
    (49, ("10d20", "3x3")),
    (50, ("12d20", "3x3")),
]


def get_level_data(level):
    if level >= 50:
        return level_data[-1]
    index = (level - 1) // 6
    index = min(index, len(level_data) - 1)
    return level_data[index]


def get_rarity(roll: int) -> Rarity:
    for (range_start, range_end), rarity in roll_rarity:
        if range_start <= roll <= range_end:
            return rarity
    raise ValueError("Roll value must be between 1 and 100")


class GrenadeCreate(BaseModel):
    rarity: Rarity
    manufacturer: Manufacturer

    manufacturer_effect: str
    primer_effect: str
    detonater_effect: str

    red_text_name: Optional[str]
    red_text_description: Optional[str]

    damage: str
    radius: str


@router.post("/generate")
def generate_grenade(
    create_result: random_create_result, session: SessionDep
) -> roll_response:

    rarity_roll = create_result.get_roll_for_label("Rarity roll")[0]
    rarity = get_rarity(rarity_roll)

    # skullduger grenades bestaan niet, dus skip index 0 (roll is van 1-8 zonder 0)
    manufacturer_roll = create_result.get_roll_for_label("Manufacturer")[0]
    manufacturer = ManufacturerIndexed[manufacturer_roll]

    manufacturer_text = manufacturer_data[manufacturer][rarity]

    # skullduger grenades bestaan niet, dus skip index 0
    grenade_primer_roll = create_result.get_roll_for_label("Grenade primer")[0]
    primer = primer_data[ManufacturerIndexed[grenade_primer_roll]]

    # skullduger grenades bestaan niet, dus skip index 0
    detonator_roll = create_result.get_roll_for_label("detonator")[0]
    detonator = detonator_data[ManufacturerIndexed[detonator_roll]]

    redtext_roll = create_result.get_roll_for_label("Redtext")[0] - 1
    redtext_name = None
    redtext_text = None
    if rarity == Rarity.LEGENDARY:
        redtext_name = redtext[redtext_roll][0]
        redtext_text = redtext[redtext_roll][1]

    data = get_level_data(create_result.level)

    newgrande = GrenadeCreate(
        rarity=rarity,
        manufacturer=manufacturer,
        manufacturer_effect=manufacturer_text,
        primer_effect=primer,
        detonater_effect=detonator,
        red_text_name=redtext_name,
        red_text_description=redtext_text,
        damage=data[1][0],
        radius=data[1][1],
    )
    gren = create_grenade(grenade_data=newgrande, session=session)
    return roll_response(item_id=gren.id, item_type="grenade")


@router.post("/")
def create_grenade(grenade_data: GrenadeCreate, session: SessionDep) -> Grenade:
    gren = Grenade(
        id=str(uuid.uuid4()),
        name="",
        description="",
        rarity=grenade_data.rarity,
        manufacturer=grenade_data.manufacturer,
        manufacturer_effect=grenade_data.manufacturer_effect,
        primer_effect=grenade_data.primer_effect,
        detonater_effect=grenade_data.detonater_effect,
        red_text_name=grenade_data.red_text_name,
        red_text_description=grenade_data.red_text_description,
        damage=grenade_data.damage,
        radius=grenade_data.radius,
    )
    session.add(gren)
    session.commit()
    session.refresh(gren)
    return gren


@router.put("/{grenade_id}", response_model=Grenade)
def update_grenade(grenade_id: str, grenade: Grenade, session: SessionDep) -> Grenade:
    statement = select(Grenade).where(Grenade.id == grenade_id)
    results = session.exec(statement)
    grenade_db = results.one()
    grenade_db.id = grenade.id
    grenade_db.name = grenade.name
    grenade_db.description = grenade.description
    grenade_db.rarity = grenade.rarity
    grenade_db.manufacturer = grenade.manufacturer
    grenade_db.manufacturer_effect = grenade.manufacturer_effect
    grenade_db.primer_effect = grenade.primer_effect
    grenade_db.detonater_effect = grenade.detonater_effect
    grenade_db.red_text_name = grenade.red_text_name
    grenade_db.red_text_description = grenade.red_text_description
    grenade_db.damage = grenade.damage
    grenade_db.radius = grenade.radius

    session.add(grenade_db)
    session.commit()
    session.refresh(grenade_db)
    return grenade_db
