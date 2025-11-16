from datetime import datetime
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from rollers.gunroller import GunRoller
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
    return GunRoller.get_roll_description()


@router.post("/generate")
def roll_gun(create_result: random_create_result, session: SessionDep) -> roll_response:

    gotten_gun = create_gun(gun_data=GunRoller.generate(create_result), session=session)
    return roll_response(item_id=gotten_gun.id, item_type="gun")


@router.get("/{gun_id}", response_model=Gun)
def get_gun(gun_id: str, session: SessionDep) -> Gun:
    statement = select(Gun).where(Gun.id == gun_id)

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
        prefix_name=gun_data.prefix_name,
        prefix_effect=gun_data.prefix_effect,
        redtext_effect=gun_data.redtext_effect,
        redtext_name=gun_data.redtext_name,
        barrel_manufacturer=gun_data.barrel_manufacturer,
        barrel_effect=gun_data.barrel_effect,
        magazine_manufacturer=gun_data.magazine_manufacturer,
        magazine_effect=gun_data.magazine_effect,
        grip_manufacturer=gun_data.grip_manufacturer,
        grip_effect=gun_data.grip_effect,
        match_bonus=gun_data.match_bonus,
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
    return gun


@router.put("/{gun_id}", response_model=Gun)
def update_gun(gun_id: str, gun: Gun, session: SessionDep) -> Gun:
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
    gun_db.redtext_effect = gun.redtext_effect
    gun_db.redtext_name = gun.redtext_name
    gun_db.prefix_effect = gun.prefix_effect
    gun_db.prefix_name = gun.prefix_name
    gun_db.barrel_effect = gun.barrel_effect
    gun_db.barrel_manufacturer = gun.barrel_manufacturer
    gun_db.magazine_effect = gun.magazine_effect
    gun_db.magazine_manufacturer = gun.magazine_manufacturer
    gun_db.grip_effect = gun.grip_effect
    gun_db.grip_manufacturer = gun.grip_manufacturer
    gun_db.match_bonus = gun.match_bonus
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
