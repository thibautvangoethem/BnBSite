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


def get_roll_for_label(result, label):
    for roll in result.rolls:
        if roll.label == label:
            return combine_roles(roll.results)


@router.post("/generate")
def create_shield(create_result=random_create_result):

    level = create_result.level
    recharge_delay = 1

    with open("./data/shields/shield_base_values.json", "r") as file:
        base_values = json.load(file)
        for value in base_values:
            if level <= value["Level"]:
                capacity = value["Capacity"]
                recharge_rate = value["RechargeRate"]

    with open("./data/shields/shield_rarities.json", "r") as file:
        shield_rarities_data = json.load(file)
        for entry in shield_rarities_data:
            roll = get_roll_for_label("Rarity roll")
            if entry[0] <= roll and roll <= entry[1]:
                rarity = entry["name"]

    with open("./data/shields/shield_manifacturer.json", "r") as file:
        manifacturer_data = json.load(file)

        for roll in create_result.rolls:
            if roll.label == "Manufacturer":
                manufacturer = manifacturer_data[combine_roles(roll.results)]["name"]
                manufacturer_effect_data = manifacturer_data[
                    combine_roles(roll.results)
                ][rarity]

                if cap_mod := manufacturer_effect_data.get("capacity_modifier"):
                    capacity = capacity * (cap_mod / 100)

                if rate_mod := manufacturer_effect_data.get("recharge_rate_modifier"):
                    recharge_rate = recharge_rate * (rate_mod / 100)

                if delay_mod := manufacturer_effect_data.get("recharge_delay_modifier"):
                    recharge_rate = recharge_rate * (delay_mod / 100)

                manufacturer_effect = manufacturer_effect_data["special_effects"]

    with open("./data/shields/shield_battery.json", "r") as file:
        all_battery_data = json.load(file)

        roll = get_roll_for_label("Baterry")
        battery = all_battery_data[roll]
        battery_rarity_data = battery["effects"][rarity]

        if cap_mod := battery_rarity_data.get("capacity_modifier"):
            capacity = capacity * (cap_mod / 100)

        if rate_mod := battery_rarity_data.get("recharge_rate_modifier"):
            recharge_rate = recharge_rate * (rate_mod / 100)

        if delay_mod := battery_rarity_data.get("recharge_delay_modifier"):
            recharge_rate = recharge_rate * (delay_mod / 100)

        battery_effect = battery_rarity_data["special_effects"]

    with open("./data/shields/shield_capacitor.json", "r") as file:
        all_capacitor_data = json.load(file)

        roll = get_roll_for_label("Capacitor")
        capacitor = all_capacitor_data[roll]
        capacitor_rarity_data = capacitor["effects"][rarity]

        if cap_mod := capacitor_rarity_data.get("capacity_modifier"):
            capacity = capacity * (cap_mod / 100)

        if rate_mod := capacitor_rarity_data.get("recharge_rate_modifier"):
            recharge_rate = recharge_rate * (rate_mod / 100)

        if delay_mod := capacitor_rarity_data.get("recharge_delay_modifier"):
            recharge_rate = recharge_rate * (delay_mod / 100)

        capacitor_effect = capacitor_rarity_data["special_effects"]

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
