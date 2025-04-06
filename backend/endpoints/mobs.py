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


import uuid

router = APIRouter(
    prefix="/mobs",
    tags=["mobs"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/common/rolldescription", response_model=random_create_description)
def get_create_descritpion(session: SessionDep) -> random_create_description:
    description = random_create_description(
        level=False,
        selections=selection_descriptions(
            mandatory=[],
            optional=[],  # todo optional choice later
        ),
        rolls=rollswrapper(
            entries=[
                roll_description(label="The roll", diceList=[Dice.D100]),
                roll_description(label="1-25 grenade ammo", diceList=[Dice.D2]),
                roll_description(label="26-50 potion", diceList=[Dice.D2]),
                roll_description(label="51-70 shield", diceList=[Dice.D2]),
                roll_description(label="71-90 grenade", diceList=[Dice.D2]),
                roll_description(label="91-100 gunn", diceList=[Dice.D2]),
            ],
            uuid=str(uuid4()),
        ),
    )
    return description


@router.get("/elite/rolldescription", response_model=random_create_description)
def get_create_descritpion(session: SessionDep) -> random_create_description:
    description = random_create_description(
        level=False,
        selections=selection_descriptions(
            mandatory=[],
            optional=[],  # todo optional choice later
        ),
        rolls=rollswrapper(
            entries=[
                roll_description(label="The roll", diceList=[Dice.D100]),
                roll_description(label="1-10 grenade ammo", diceList=[Dice.D2]),
                roll_description(label="11-20 potion", diceList=[Dice.D2]),
                roll_description(label="21-50 shield", diceList=[Dice.D2]),
                roll_description(label="51-80 grenade", diceList=[Dice.D2]),
                roll_description(label="81-100 gunn", diceList=[Dice.D2]),
            ],
            uuid=str(uuid4()),
        ),
    )
    return description


@router.get("/mboss/rolldescription", response_model=random_create_description)
def get_create_descritpion(session: SessionDep) -> random_create_description:
    description = random_create_description(
        level=False,
        selections=selection_descriptions(
            mandatory=[],
            optional=[],  # todo optional choice later
        ),
        rolls=rollswrapper(
            entries=[
                roll_description(label="The roll", diceList=[Dice.D100]),
                roll_description(label="1-33 gun", diceList=[Dice.D2]),
                roll_description(label="34-66 grenade ", diceList=[Dice.D2]),
                roll_description(label="67-100 shield", diceList=[Dice.D2]),
            ],
            uuid=str(uuid4()),
        ),
    )
    return description
