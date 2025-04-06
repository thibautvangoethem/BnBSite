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
    prefix="/grenades",
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
                roll_description(label="Grenade primer", diceList=[Dice.D8]),
                roll_description(label="detonator", diceList=[Dice.D8]),
                roll_description(label="Redtext", diceList=[Dice.D10]),
            ],
            uuid=str(uuid4()),
        ),
    )
    return description
