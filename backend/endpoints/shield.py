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
from models.shield import Shield, ShieldRead
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
            optional=[],  # todo optional choice later
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


class random_create_result(BaseModel):
    level: int
    selections: list[selection_mandatory]
    rolls: list[roll_result]


def combine_roles(results):
    result_str = ""
    for item in results:
        result_str += str(item)

    return int(result_str)


def get_roll_for_label(rolls, label):
    for roll in rolls:
        if roll.label == label:
            return combine_roles(roll.result)


@router.post("/generate")
def create_shield(create_result: random_create_result):
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
            roll = get_roll_for_label(create_result.rolls, "Rarity roll")
            if entry["range"][0] <= roll and roll <= entry["range"][1]:
                rarity = entry["name"]

    with open(
        "./backend/models/data/shields/shield_manifacturer_effect.json", "r"
    ) as file:
        manifacturer_data = json.load(file)

        for roll in create_result.rolls:
            if roll.label == "Manufacturer":
                manufacturer = manifacturer_data[combine_roles(roll.result) - 1]["name"]
                manufacturer_effect_data = manifacturer_data[
                    combine_roles(roll.result) - 1
                ]["effects"][rarity]

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

    with open("./backend/models/data/shields/shield_battery.json", "r") as file:
        all_battery_data = json.load(file)

        roll = get_roll_for_label(create_result.rolls, "Baterry")
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

        roll = get_roll_for_label(create_result.rolls, "Capacitor")
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

    # TODO red text

    shield = Shield(
        rarity=rarity,
        manufacturer=manufacturer,
        capacity=int(capacity),
        recharge_rate=int(recharge_rate),
        recharge_delay=int(recharge_delay),
        manufacturer_effect=manufacturer_effect,
        battery_effect=battery_effect,
        capacitor_effect=capacitor_effect,
    )

    # TODO Nova damage

    shield_read = ShieldRead.model_validate(shield)

    print(f"SHIELD : {shield}")

    return shield_read
