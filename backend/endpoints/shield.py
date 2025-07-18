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
from models.shield import Shield
import random
import json

import uuid

router = APIRouter(
    prefix="/shields",
    tags=["shield"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/rolldescription", response_model=random_create_description)
def get_create_descritpion(session: SessionDep) -> random_create_description:
    description = random_create_description(
        level=True,
        selections=selection_descriptions(
            mandatory=[],
            optional=[
                selection_description(
                    label="rarity",
                    options=[member.value for member in Rarity],
                ),
                selection_description(
                    label="enforce_manufacturer",
                    # lol dat zijn niet de bnb manufacturers
                    options=[
                        "ANSHIN",
                        "PANGOLIN",
                        "HYPERION",
                        "TORGUE",
                        "VLADOFF",
                        "BANDIT",
                        "MALIWAN",
                        "TEDIORE",
                    ],
                ),
            ],  # todo optional choice later
        ),
        rolls=rollswrapper(
            entries=[
                roll_description(label="Rarity roll", diceList=[Dice.D100]),
                roll_description(label="Manufacturer", diceList=[Dice.D8]),
                roll_description(label="Capacitor", diceList=[Dice.D8]),
                roll_description(label="Baterry", diceList=[Dice.D8]),
                roll_description(label="Redtext", diceList=[Dice.D20]),
            ],
            uuid=str(uuid4()),
        ),
    )
    return description


manufacturer_to_number = {
    "ANSHIN": 0,
    "PANGOLIN": 1,
    "HYPERION": 2,
    "TORGUE": 3,
    "VLADOFF": 4,
    "BANDIT": 5,
    "MALIWAN": 6,
    "TEDIORE": 7,
}


@router.post("/generate")
def create_shield(
    create_result: random_create_result, session: SessionDep
) -> roll_response:
    print(f"TESTING --- {create_result}")
    level = create_result.level
    recharge_delay = 1

    import os

    print(os.getcwd())
    with open("./backend/models/data/shields/shield_base_values.json", "r") as file:
        base_values = json.load(file)
        for value in base_values:
            if value["Level"][0] <= level and level <= value["Level"][-1]:
                capacity = value["Capacity"]
                print(f"CAPACITY {capacity}")
                recharge_rate = value["RechargeRate"]
                print(f"RATE {recharge_rate}")
                break

    with open("./backend/models/data/shields/shield_rarities.json", "r") as file:
        shield_rarities_data = json.load(file)
        for entry in shield_rarities_data:
            roll = create_result.get_roll_for_label("Rarity roll")[0]
            if entry["range"][0] <= roll and roll <= entry["range"][1]:
                rarity = entry["name"]
    rarity_choice = create_result.get_option_for_label("rarity")
    if not (rarity_choice == None or len(rarity_choice) == 0):
        rarity = rarity_choice[0].upper()

    nova_damage = None
    nova_element = None
    with open(
        "./backend/models/data/shields/shield_manifacturer_effect.json", "r"
    ) as file:
        manifacturer_data = json.load(file)

        roll = create_result.get_roll_for_label("Manufacturer")

        manufacturer_choice = create_result.get_option_for_label("enforce_manufacturer")
        if not (manufacturer_choice == None or len(manufacturer_choice) == 0):
            # yup de roll data aanpassen is hier de properste optie
            roll[0] = manufacturer_to_number[manufacturer_choice[0]] + 1

        manufacturer = manifacturer_data[roll[0] - 1]["name"]
        manufacturer_effect_data = manifacturer_data[roll[0] - 1]["effects"][rarity]

        if cap_mod := manufacturer_effect_data.get("capacity_modifier"):
            capacity = capacity * (1 + (cap_mod / 100))

        if rate_mod := manufacturer_effect_data.get("recharge_rate_modifier"):
            recharge_rate = recharge_rate * (1 + (rate_mod / 100))

        if delay_mod := manufacturer_effect_data.get("recharge_delay_modifier"):
            recharge_rate = recharge_rate * (1 + (delay_mod / 100))

        manufacturer_effect = manufacturer_effect_data.get("special_effects")
        if manufacturer_effect:
            manufacturer_effect = manufacturer_effect[0]
        if manufacturer_effect == []:
            manufacturer_effect = None

        if manufacturer_effect_data.get("scales_with_level"):
            if manufacturer_effect_data.get("element_roll"):
                elemental_rolls = [
                    "fire",
                    "shock",
                    "corrosive",
                    "cryo",
                    "radiation",
                    "choose",
                ]
                nova_element = elemental_rolls[random.randint(0, 5)]

            with open(
                "./backend/models/data/shields/shield_nova_dmg.json",
                "r",
            ) as file2:
                nova_damage_data = json.load(file2)
                for value in nova_damage_data:
                    if value["Level"][0] <= level and level <= value["Level"][-1]:
                        nova_damage = value["damage"]
                        break

    with open("./backend/models/data/shields/shield_battery.json", "r") as file:
        all_battery_data = json.load(file)

        roll = create_result.get_roll_for_label("Baterry")[0]
        battery = all_battery_data[roll - 1]
        battery_rarity_data = battery["effects"][rarity]

        if cap_mod := battery_rarity_data.get("capacity_modifier"):
            capacity = capacity * (1 + (cap_mod / 100))

        if rate_mod := battery_rarity_data.get("recharge_rate_modifier"):
            recharge_rate = recharge_rate * (1 + (rate_mod / 100))

        if delay_mod := battery_rarity_data.get("recharge_delay_modifier"):
            recharge_rate = recharge_rate * (1 + (delay_mod / 100))

        # TODO needs to work to cast to string instead of list
        battery_effect = battery_rarity_data.get("special_effects")
        if battery_effect:
            battery_effect = battery_effect[0]

    with open("./backend/models/data/shields/shield_capacitor.json", "r") as file:
        all_capacitor_data = json.load(file)

        roll = create_result.get_roll_for_label("Capacitor")[0]
        capacitor = all_capacitor_data[roll - 1]
        capacitor_rarity_data = capacitor["effects"][rarity]

        if cap_mod := capacitor_rarity_data.get("capacity_modifier"):
            capacity = capacity * (1 + (cap_mod / 100))

        if rate_mod := capacitor_rarity_data.get("recharge_rate_modifier"):
            recharge_rate = recharge_rate * (1 + (rate_mod / 100))

        if delay_mod := capacitor_rarity_data.get("recharge_delay_modifier"):
            recharge_rate = recharge_rate * (1 + (delay_mod / 100))

        capacitor_effect = capacitor_rarity_data.get("special_effects")
        if capacitor_effect:
            capacitor_effect = capacitor_effect[0]

    red_text_name = None
    red_text_description = None
    if create_result.get_roll_for_label("Rarity roll")[0] >= 96:
        with open("./backend/models/data/shields/shield_red_text.json", "r") as file:
            all_red_text_data = json.load(file)

            roll = create_result.get_roll_for_label("Redtext")[0]
            red_text_data = all_red_text_data[roll - 1]
            red_text_name = red_text_data["name"]
            red_text_description = red_text_data["description"]

            if cap_mod := red_text_data.get("capacity_modifier"):
                capacity = capacity * (1 + (cap_mod / 100))

            if rate_mod := red_text_data.get("recharge_rate_modifier"):
                recharge_rate = recharge_rate * (1 + (rate_mod / 100))

            if delay_mod := red_text_data.get("recharge_delay_modifier"):
                recharge_rate = recharge_rate * (1 + (delay_mod / 100))

    shield = Shield(
        id=str(uuid.uuid4()),
        rarity=rarity,
        manufacturer=manufacturer,
        capacity=int(capacity),
        recharge_rate=int(recharge_rate),
        recharge_delay=int(recharge_delay),
        manufacturer_effect=manufacturer_effect,
        battery_effect=battery_effect,
        capacitor_effect=capacitor_effect,
        red_text_name=red_text_name,
        red_text_description=red_text_description,
        nova_damage=nova_damage,
        nova_element=nova_element,
    )

    print(f"SHIELD : {shield}")

    session.add(shield)
    session.commit()
    session.refresh(shield)

    print(f"SHIELD : {shield}")

    return roll_response(item_id=shield.id, item_type="shield")


@router.get("/{shield_id}", response_model=Shield)
def get_shield(shield_id: str, session: SessionDep) -> Shield:
    statement = select(Shield).where(Shield.id == shield_id)

    shield = session.exec(statement).first()

    if shield is None:
        raise HTTPException(status_code=404, detail="shield not found")

    return shield


@router.put("/{shield_id}", response_model=Shield)
def update_shield(shield_id: str, shield: Shield, session: SessionDep) -> Shield:
    statement = select(Shield).where(Shield.id == shield_id)
    results = session.exec(statement)
    shield_db = results.one()
    shield_db.id = shield.id
    shield_db.name = shield.name
    shield_db.description = shield.description
    shield_db.rarity = shield.rarity
    shield_db.manufacturer = shield.manufacturer
    shield_db.capacity = shield.capacity
    shield_db.recharge_rate = shield.recharge_rate
    shield_db.recharge_delay = shield.recharge_delay
    shield_db.manufacturer_effect = shield.manufacturer_effect
    shield_db.capacitor_effect = shield.capacitor_effect
    shield_db.battery_effect = shield.battery_effect
    shield_db.red_text_name = shield.red_text_name
    shield_db.red_text_description = shield.red_text_description
    shield_db.nova_damage = shield.nova_damage
    shield_db.nova_element = shield.nova_element

    session.add(shield_db)
    session.commit()
    session.refresh(shield_db)
    return shield_db
