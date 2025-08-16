from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from models.classmod import *
from models.common import *
from appglobals import SessionDep, oauth2_scheme
from sqlmodel import select
from sqlalchemy.orm import selectinload
from models.roll_data import *
from uuid import uuid4
from models.grenade import Grenade
from models.rollhistory import RollHistory
from datetime import datetime

import uuid

router = APIRouter(
    prefix="/classmods",
    tags=["classmods"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

prefix_data = {
    0: [
        "Talented",
        {
            Rarity.COMMON: "+1 Mastery",
            Rarity.UNCOMMON: "+2 Mastery",
            Rarity.RARE: "+3 Mastery",
            Rarity.EPIC: "+4 Mastery",
            Rarity.LEGENDARY: "+5 Mastery",
        },
    ],
    1: [
        "Sharp-eyed",
        {
            Rarity.COMMON: "+1 Accuracy",
            Rarity.UNCOMMON: "+2 Accuracy",
            Rarity.RARE: "+3 Accuracy",
            Rarity.EPIC: "+4 Accuracy",
            Rarity.LEGENDARY: "+5 Accuracy",
        },
    ],
    2: [
        "Heavy-Hitting",
        {
            Rarity.COMMON: "+1 Damage",
            Rarity.UNCOMMON: "+2 Damage",
            Rarity.RARE: "+3 Damage",
            Rarity.EPIC: "+4 Damage",
            Rarity.LEGENDARY: "+5 Damage",
        },
    ],
    3: [
        "Quick",
        {
            Rarity.COMMON: "+1 Speed",
            Rarity.UNCOMMON: "+2 Speed",
            Rarity.RARE: "+3 Speed",
            Rarity.EPIC: "+4 Speed",
            Rarity.LEGENDARY: "+5 Speed",
        },
    ],
    4: [
        "Salvaging",
        {
            Rarity.COMMON: "+1 Hits on lowest accuracy rolls",
            Rarity.UNCOMMON: "+2 Hits on lowest accuracy rolls",
            Rarity.RARE: "+3 Hits on lowest accuracy rolls",
            Rarity.EPIC: "+4 Hits on lowest accuracy rolls",
            Rarity.LEGENDARY: "+5 Hits on lowest accuracy rolls",
        },
    ],
    5: [
        "Bare-Knuckled",
        {
            Rarity.COMMON: "+1 Melee Hits",
            Rarity.UNCOMMON: "+2 Melee Hits",
            Rarity.RARE: "+3 Melee Hits",
            Rarity.EPIC: "+4 Melee Hits",
            Rarity.LEGENDARY: "+5 Melee Hits",
        },
    ],
    6: [
        "High Rolling",
        {
            Rarity.COMMON: "+1 Crit die on high accuracy roll",
            Rarity.UNCOMMON: "+2 Crit die on high accuracy roll",
            Rarity.RARE: "+3 Crit die on high accuracy roll",
            Rarity.EPIC: "+4 Crit die on high accuracy roll",
            Rarity.LEGENDARY: "+5 Crit die on high accuracy roll",
        },
    ],
    7: [
        "Average",
        {
            Rarity.COMMON: "+1 damage die on medium accuracy roll",
            Rarity.UNCOMMON: "+2 damage die on medium accuracy roll",
            Rarity.RARE: "+3 damage die on medium accuracy roll",
            Rarity.EPIC: "+4 damage die on medium accuracy roll",
            Rarity.LEGENDARY: "+5 damage die on medium accuracy roll",
        },
    ],
    8: [
        "Beefy",
        {
            Rarity.COMMON: "+10% Health",
            Rarity.UNCOMMON: "+20% Health",
            Rarity.RARE: "+30% Health",
            Rarity.EPIC: "+40% Health",
            Rarity.LEGENDARY: "+50% Health",
        },
    ],
    9: [
        "Covering",
        {
            Rarity.COMMON: "+10% Shield",
            Rarity.UNCOMMON: "+20% Shield",
            Rarity.RARE: "+30% Shield",
            Rarity.EPIC: "+40% Shield",
            Rarity.LEGENDARY: "+50% Shield",
        },
    ],
}


suffix_data = {
    "Warden": {
        "description": "Warden",
        "effects": {
            Rarity.COMMON: "+1 Speed, +10% shield",
            Rarity.UNCOMMON: "+1 Speed, +15% shield",
            Rarity.RARE: "+2 Speed, +20% shield",
            Rarity.EPIC: "+3 Speed, +50% shield",
            Rarity.LEGENDARY: "+5 Speed, +50% shield & You can transfer HP to shield and vice versa",
        },
    },
    "Nurse": {
        "description": "Nurse",
        "effects": {
            Rarity.COMMON: "Allies receive your full health regen bonus",
            Rarity.UNCOMMON: "Allies receive half of your health regen +50 health regen",
            Rarity.RARE: "Allies receive your full health regen bonus +100 health regen",
            Rarity.EPIC: "Allies receive twice your health regen bonus +150 health regen",
            Rarity.LEGENDARY: "Regen half your max hp each turn, whenever you kill an enemy, you can allocate his max hp between yourself and allies as health or bonus hp if you are full",
        },
    },
    "Sorcerer": {
        "description": "Sorcerer",
        "effects": {
            Rarity.COMMON: "Gain an extra elemental die when dealing elemental damage (biggest possible die)",
            Rarity.UNCOMMON: "Gain 2 extra elemental die when dealing elemental damage (biggest possible die)",
            Rarity.RARE: "Gain 3 extra elemental die when dealing elemental damage (biggest possible die)",
            Rarity.EPIC: "Gain 3 extra elemental die of your choice when dealing elemental damage (biggest possible die)",
            Rarity.LEGENDARY: "Gain 3 extra elemental die of your choice when dealing damage (biggest possible die) & Action skill elemental damage is doubled, whenever you use your action skill, apply the element damage on all enemies on the battlefield",
        },
    },
    "Engineer": {
        "description": "Engineer",
        "effects": {
            Rarity.COMMON: "+1 Mastery, +1 hits by action skill",
            Rarity.UNCOMMON: "+2 Mastery, +1 hits by action skill",
            Rarity.RARE: "+2 Mastery, +3 hits by action skill",
            Rarity.EPIC: "+3 Mastery, +4 hits by action skill",
            Rarity.LEGENDARY: "+5 Mastery, +5 hits by action skill & Kill made by your action skill reset the duration and grant it a stacking extra damage die",
        },
    },
    "Ranger": {
        "description": "Ranger",
        "effects": {
            Rarity.COMMON: "+1 Damage, +1 Accuracy",
            Rarity.UNCOMMON: "+1 Damage, +2 Accuracy",
            Rarity.RARE: "+2 Damage, +2 Accuracy",
            Rarity.EPIC: "+3 Damage, +3 Accuracy",
            Rarity.LEGENDARY: "+5 Damage, +4 Accuracy & grenade kills allow you to attack again for free, gun kills grant you 1 grenade ammo",
        },
    },
    "Sentinel": {
        "description": "Sentinel",
        "effects": {
            Rarity.COMMON: "+10% shield, +10% Health",
            Rarity.UNCOMMON: "+15% shield, +15% Health",
            Rarity.RARE: "+15% shield, +25% Health",
            Rarity.EPIC: "+20% shield, +30% Health",
            Rarity.LEGENDARY: "+25% shield, +35% Health & When an ally next to you takes damage, you can choose to take the damage yourself and immediately do a free attack on that enemy",
        },
    },
    "Hunter": {
        "description": "Hunter",
        "effects": {
            Rarity.COMMON: "+1 Acc, +1 DMG",
            Rarity.UNCOMMON: "+2 Acc, +1 DMG",
            Rarity.RARE: "+2 Acc, +2 DMG",
            Rarity.EPIC: "+3 Acc, +3 DMG",
            Rarity.LEGENDARY: "+4 Acc, +5 DMG & You can hit all enemies as long as they are in range of an ally",
        },
    },
    "Scavenger": {
        "description": "Scavenger",
        "effects": {
            Rarity.COMMON: "+1 Speed, +1 max grenade capacity",
            Rarity.UNCOMMON: "+2 Speed, +1 max grenade capacity",
            Rarity.RARE: "+3 Speed, +2 max grenade capacity",
            Rarity.EPIC: "+4 Speed, +3 max grenade capacity",
            Rarity.LEGENDARY: "+5 Speed, +4 max grenade capacity & Upon activation and ending of your action skill, it drops a grenade in its space (grenades dropped this way won't damage allies)",
        },
    },
    "Duelist": {
        "description": "Duelist",
        "effects": {
            Rarity.COMMON: "+1 DMG, +10% hp",
            Rarity.UNCOMMON: "+2 DMG, +10% hp",
            Rarity.RARE: "+3 DMG, +25% hp",
            Rarity.EPIC: "+4 DMG, +25% hp",
            Rarity.LEGENDARY: "+5 DMG, +25% hp & if the enemy you last attacked, attacks someone else then you, you can activate (capstone gunslinger tree) for free on that enemy",
        },
    },
    "Raider": {
        "description": "Raider",
        "effects": {
            Rarity.COMMON: "+3 Accuracy with assault rifles and shotguns",
            Rarity.UNCOMMON: "+5 Accuracy with assault rifles and shotguns",
            Rarity.RARE: "+5 Accuracy with assault rifles and shotguns, +3 DMG",
            Rarity.EPIC: "+7 Accuracy with assault rifles and shotguns, +4 DMG",
            Rarity.LEGENDARY: "+10 Accuracy with assault rifles and shotguns, +5 DMG & Kills with Shotguns grant you a stacking +1 Speed, Kills with Assault Rifles grant you a stacking +5% max hp, stacks go away when you haven't killed an enemy in 2 turns. ",
        },
    },
    "Hoarder": {
        "description": "Hoarder",
        "effects": {
            Rarity.COMMON: "+1 Hit die for every piece of unused gear in your inventory",
            Rarity.UNCOMMON: "+2 Hit die for every piece of unused gear in your inventory",
            Rarity.RARE: "+4 Hit die for every piece of unused gear in your inventory",
            Rarity.EPIC: "+5 Hit die for every piece of unused gear in your inventory, +2 Speed",
            Rarity.LEGENDARY: "+5 Hit die for every piece of unused gear in your inventory, +3 Speed & Looting a chest gives you double damage next round",
        },
    },
    "Tank": {
        "description": "Tank",
        "effects": {
            Rarity.COMMON: "+5% max health regen",
            Rarity.UNCOMMON: "+10% max health regen, +5% max hp",
            Rarity.RARE: "+20% max health regen, +10% max hp",
            Rarity.EPIC: "+25% max health regen, +20% max hp",
            Rarity.LEGENDARY: "+30% max health regen, +25% max hp & At full health, health regen turns into kinetic damage at the nearest enemy of choice.",
        },
    },
    "Berserker": {
        "description": "Berserker",
        "effects": {
            Rarity.COMMON: "+1 Melee hit, +1 Melee die",
            Rarity.UNCOMMON: "+2 Melee hit, +1 Melee die",
            Rarity.RARE: "+3 Melee hit, +2 Melee die",
            Rarity.EPIC: "+4 Melee hit, +3 Melee die",
            Rarity.LEGENDARY: "+5 Melee hit, +5 Melee die & Every tenth melee attack deals 500% damage",
        },
    },
    "Slab": {
        "description": "Slab",
        "effects": {
            Rarity.COMMON: "+10% max HP, +10% shield capacity",
            Rarity.UNCOMMON: "+20% max HP, +10% shield capacity",
            Rarity.RARE: "+25% max HP, +20% shield capacity",
            Rarity.EPIC: "+35% max HP, +25% shield capacity",
            Rarity.LEGENDARY: "+50% max HP, +50% shield capacity & You can choose to drain 5% of your shields to add it to your next melee/explosive attack",
        },
    },
    "Blaster": {
        "description": "Blaster",
        "effects": {
            Rarity.COMMON: "+3 Damage with launchers",
            Rarity.UNCOMMON: "+3 Damage and 2 ACC with launchers",
            Rarity.RARE: "+3 Damage and 5 ACC with launchers",
            Rarity.EPIC: "+4 Damage and 4 ACC with launchers",
            Rarity.LEGENDARY: "+5 Damage and 5 ACC with launchers & Kills with launchers cause an aftershock, dealing the damage again in a 3x3 radius",
        },
    },
    "Reaper": {
        "description": "Reaper",
        "effects": {
            Rarity.COMMON: "+2 to all stats while a kill skill is active",
            Rarity.UNCOMMON: "+4 to all stats while a kill skill is active",
            Rarity.RARE: "+6 to all stats while a kill skill is active",
            Rarity.EPIC: "+8 to all stats while a kill skill is active",
            Rarity.LEGENDARY: "+10 to all stats while a kill skill is active & Activating your action skill counts as getting a kill skill",
        },
    },
    "Sickle": {
        "description": "Sickle",
        "effects": {
            Rarity.COMMON: "+4 Melee damage die",
            Rarity.UNCOMMON: "+6 Melee damage die",
            Rarity.RARE: "+10 Melee damage die",
            Rarity.EPIC: "+10 Melee damage die, melee crits on an attack roll of 15+",
            Rarity.LEGENDARY: "+10 Melee damage die, melee crits on an attack roll of 10+ & Upon entering FFYL, Your next Melee attack is ranged, deals triple damage, and on kill places you on the enemy you just killed",
        },
    },
    "Torch": {
        "description": "Torch",
        "effects": {
            Rarity.COMMON: "+2 fire damage die while dealing fire damage (highest possible die)",
            Rarity.UNCOMMON: "+2 fire damage die while dealing fire damage (highest possible die), doubled while on fire",
            Rarity.RARE: "+3 fire damage die while dealing fire damage (highest possible die), doubled while on fire",
            Rarity.EPIC: "+3 fire damage die while dealing fire damage (highest possible die), tripled while on fire",
            Rarity.LEGENDARY: "+5 fire damage die while dealing fire damage (highest possible die), tripled while on fire & Fire damage now heals you, and still counts as damage for relevant skills",
        },
    },
    "Sniper": {
        "description": "Assassin",
        "effects": {
            Rarity.COMMON: "+1 ACC, +2 DMG with snipers",
            Rarity.UNCOMMON: "+2 ACC, +3 DMG with snipers",
            Rarity.RARE: "+3 ACC, +5 DMG with snipers",
            Rarity.EPIC: "+5 ACC, +7 DMG with snipers",
            Rarity.LEGENDARY: "+7 ACC, +8 DMG with snipers & Excess accuracy (amount above 20) on an attack roll is doubled and added to your crit damage",
        },
    },
    "Rogue": {
        "description": "Rogue",
        "effects": {
            Rarity.COMMON: "+1 Speed, +1 Mastery",
            Rarity.UNCOMMON: "+2 Speed, +2 Mastery",
            Rarity.RARE: "+4 Speed, +2 Mastery",
            Rarity.EPIC: "+4 Speed, +4 Mastery",
            Rarity.LEGENDARY: "+5 Speed, +5 Mastery & Allies attacking the target you attack after using an action skill, receive 2 extra crit die",
        },
    },
    "Ninja": {
        "description": "Ninja",
        "effects": {
            Rarity.COMMON: "Melee hit die for melee attacks is now a D10",
            Rarity.UNCOMMON: "Melee hit die for melee attacks is now a D12, +1 Melee hit die",
            Rarity.RARE: "Melee hit die for melee attacks is now a D12, +2 Melee hit die",
            Rarity.EPIC: "Melee hit die for melee attacks is now a D12, +4 Melee hit die",
            Rarity.LEGENDARY: "Melee hit die for melee attacks is now a D12, +5 Melee hit die & On melee kills instantly recharge 20% of your shield and an action skill use",
        },
    },
}

roll_rarity = [
    ((1, 40), Rarity.COMMON),
    ((41, 70), Rarity.UNCOMMON),
    ((71, 85), Rarity.RARE),
    ((86, 95), Rarity.EPIC),
    ((96, 100), Rarity.LEGENDARY),
]


def get_rarity(roll: int) -> Rarity:
    for (range_start, range_end), rarity in roll_rarity:
        if range_start <= roll <= range_end:
            return rarity
    raise ValueError("Roll value must be between 1 and 100")


class_suffix_mapping = {
    Classes.SIREN: ["Warden", "Nurse", "Sorcerer"],
    Classes.COMMANDO: ["Engineer", "Ranger", "Sentinel"],
    Classes.HUNTER: ["Hunter", "Scavenger", "Duelist"],
    Classes.GUNZERKER: ["Raider", "Hoarder", "Tank"],
    Classes.BERSERKER: ["Berserker", "Slab", "Blaster"],
    Classes.PSYCHO: ["Reaper", "Sickle", "Torch"],
    Classes.ASSASSIN: ["Sniper", "Rogue", "Ninja"],
}


@router.get("/rolldescription", response_model=random_create_description)
def get_create_descritpion(session: SessionDep) -> random_create_description:
    description = random_create_description(
        level=False,
        selections=selection_descriptions(
            mandatory=[],
            optional=[
                selection_description(
                    label="Rarity",
                    options=[
                        member.value for member in Rarity if member != Rarity.UNIQUE
                    ],
                ),
                selection_description(
                    label="Enforce Class",
                    options=[
                        member.value
                        for member in Classes
                        if member != Classes.MECHROMANCER
                    ],
                ),
            ],
        ),
        rolls=rollswrapper(
            entries=[
                roll_description(label="Rarity roll", diceList=[Dice.D100]),
                roll_description(label="class", diceList=[Dice.D6, Dice.D10]),
                roll_description(label="prefix", diceList=[Dice.D10]),
                roll_description(label="suffix", diceList=[Dice.D12]),
            ],
            uuid=str(uuid4()),
        ),
    )
    return description


class ClassModCreate(BaseModel):
    rarity: Rarity
    class_type: Classes
    prefix: str
    prefix_effect: str
    suffix: str
    suffix_effect: str


def map_classrol_to_class(rollnumber: int) -> Classes:
    # slighlty below 7 so 60 doesnt match to index 7
    divider = 60.0 / 6.99999
    # mappings:
    # 0 -> [1-8] 8
    # 1 -> [9-17] 9
    # 2 -> [18-25] 8
    # 3 -> [26-34] 9
    # 4 -> [35-42] 8
    # 5 -> [43-51] 9
    # 56 -> [52-60] 9
    index = float(rollnumber) / divider
    index = int(index)
    return ClassIndexed[index]


@router.post("/generate")
def generate_classmod(
    create_result: random_create_result, session: SessionDep
) -> roll_response:

    # rarity
    rarity_roll = create_result.get_roll_for_label("Rarity roll")[0]
    rarity = get_rarity(rarity_roll)
    rarity_choice = create_result.get_option_for_label("Rarity")
    if not (rarity_choice == None or len(rarity_choice) == 0):
        rarity = Rarity(rarity_choice[0])

    # class roll
    class_rolls = create_result.get_roll_for_label("class")
    clazz = map_classrol_to_class(class_rolls[0] * class_rolls[1])
    class_choice = create_result.get_option_for_label("Enforce Class")
    if not (class_choice == None or len(class_choice) == 0):
        clazz = Classes(class_choice[0])

    # prefix
    prefix_roll = create_result.get_roll_for_label("prefix")[0]
    prefix_entry = prefix_data[prefix_roll - 1]
    prefix_name = prefix_entry[0]
    prefix_effect = prefix_entry[1][rarity]

    # suffix
    suffix_roll = create_result.get_roll_for_label("suffix")[0]
    suffix_index = int((suffix_roll - 1) / 4)
    suffix_name = class_suffix_mapping[clazz][suffix_index]
    suffix_effect = suffix_data[suffix_name]["effects"][rarity]

    newClassMod = ClassModCreate(
        rarity=rarity,
        class_type=clazz,
        prefix=prefix_name,
        prefix_effect=prefix_effect,
        suffix=suffix_name,
        suffix_effect=suffix_effect,
    )
    clm = create_classmod(classmod_data=newClassMod, session=session)
    return roll_response(item_id=clm.id, item_type="classmod")


@router.post("/")
def create_classmod(classmod_data: ClassModCreate, session: SessionDep) -> ClassMod:
    cl = ClassMod(
        id=str(uuid.uuid4()),
        name=f"{classmod_data.rarity.value} {classmod_data.prefix} {classmod_data.suffix}",
        description="",
        rarity=classmod_data.rarity,
        class_type=classmod_data.class_type,
        prefix=classmod_data.prefix,
        prefix_effect=classmod_data.prefix_effect,
        suffix=classmod_data.suffix,
        suffix_effect=classmod_data.suffix_effect,
    )
    session.add(cl)
    histoir = RollHistory(
        id=cl.id, date=datetime.now(), description=str(cl), type="Classmod"
    )
    session.add(histoir)
    session.commit()
    session.refresh(cl)

    return cl


@router.put("/{classmod_id}", response_model=ClassMod)
def update_classmod(
    classmod_id: str, classmod: ClassMod, session: SessionDep
) -> ClassMod:
    statement = select(ClassMod).where(ClassMod.id == classmod_id)
    results = session.exec(statement)
    cl_db = results.one()
    cl_db.id = classmod.id
    cl_db.name = classmod.name
    cl_db.description = classmod.description
    cl_db.rarity = classmod.rarity
    cl_db.class_type = classmod.class_type
    cl_db.prefix = classmod.prefix
    cl_db.prefix_effect = classmod.prefix_effect
    cl_db.suffix = classmod.suffix
    cl_db.suffix_effect = classmod.suffix_effect

    session.add(cl_db)
    session.commit()
    session.refresh(cl_db)
    return cl_db


@router.get("/{classmod_id}", response_model=ClassMod)
def get_classmod(classmod_id: str, session: SessionDep) -> ClassMod:
    statement = select(ClassMod).where(ClassMod.id == classmod_id)

    classmod = session.exec(statement).first()

    if classmod is None:
        raise HTTPException(status_code=404, detail="classmod not found")

    return classmod
