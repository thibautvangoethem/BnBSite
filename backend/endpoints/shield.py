from datetime import datetime
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from rollers.shieldroller import ShieldRoller
from models.rollhistory import RollHistory
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
    return ShieldRoller.get_roll_description()


@router.post("/generate")
def create_shield(
    create_result: random_create_result, session: SessionDep
) -> roll_response:

    shield = ShieldRoller.generate(create_result)

    print(f"SHIELD : {shield}")

    session.add(shield)
    histoir = RollHistory(
        id=shield.id, date=datetime.now(), description=str(shield), type="Shield"
    )
    session.add(histoir)
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
