from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from models.vendor import *
from models.common import *
from appglobals import SessionDep, oauth2_scheme
from sqlmodel import select
from sqlalchemy.orm import selectinload
from models.roll_data import *
from uuid import uuid4
from models.grenade import Grenade
from models.rollhistory import RollHistory
import random
from datetime import datetime

import uuid

router = APIRouter(
    prefix="/vendors",
    tags=["vendors"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def roll_item(item_type: str) -> RollHistory:
    item_type = item_type.lower()
    if item_type == "gun":
        pass
    elif item_type == "grenade":
        pass
    elif item_type == "shield":
        pass
    elif item_type == "potion":
        pass
    elif item_type == "classmod":
        pass


class vendor_return(BaseModel):
    # general metadata
    id: str = Field(primary_key=True)
    name: str = ""
    description: str = None
    quote: str = ""  # single quote chosen

    # data about currently in stock items
    item_of_the_day: RollHistory
    normal_items: list[RollHistory]
    bought_items: list[str]  # multiple ; delimeted ids


@router.get("/{vendor_id}/reroll_normal", response_model=Vendor)
def rerollvendorNormal(vendor_id: str, session: SessionDep) -> vendor_return:
    rolled_items = list()

    return get_vendor(vendor_id, session)


@router.get("/{vendor_id}/reroll_iod", response_model=vendor_return)
def rerollvendoriod(vendor_id: str, session: SessionDep) -> vendor_return:
    statement = select(Vendor).where(Vendor.id == vendor_id)
    vendor = session.exec(statement).first()
    if vendor is None:
        raise HTTPException(status_code=404, detail="vendor not found")

    temp = vendor.bought_items.split(";")
    temp.remove(vendor.item_of_the_day)
    vendor.bought_items = ";".join(temp)

    chosen_item = random.choice(vendor.supported_items.split(";"))

    return get_vendor(vendor_id, session)


@router.get("/{vendor_id}/buy/{item_id}", response_model=vendor_return)
def buyitem(vendor_id: str, item_id: str, session: SessionDep) -> vendor_return:
    statement = select(Vendor).where(Vendor.id == vendor_id)

    vendor = session.exec(statement).first()
    if vendor is None:
        raise HTTPException(status_code=404, detail="vendor not found")
    if not (
        (vendor.item_of_the_day is not None and vendor.item_of_the_day == item_id)
        or (vendor.normal_items is not None and item_id in vendor.normal_items)
    ):
        raise HTTPException(
            status_code=422,
            detail=f"vendor {vendor_id} does not have an item with id {item_id} for sale",
        )

    if item_id in vendor.bought_items:
        raise HTTPException(
            status_code=422,
            detail=f"item {item_id} has already been sold to someone",
        )
    vendor.bought_items += f";{item_id}"

    session.add(vendor)
    session.commit()
    session.refresh(vendor)

    return get_vendor(vendor_id, session)


@router.get("/{vendor_id}", response_model=vendor_return)
def get_vendor(vendor_id: str, session: SessionDep) -> vendor_return:
    statement = select(Vendor).where(Vendor.id == vendor_id)

    vendor = session.exec(statement).first()

    if vendor is None:
        raise HTTPException(status_code=404, detail="vendor not found")

    chosen_quote = random.choice(vendor.quotes.split(";"))
    statement = select(RollHistory).where(RollHistory.id == vendor.item_of_the_day)
    iod = session.exec(statement).first()
    statement = select(RollHistory).where(RollHistory.id in vendor.normal_items)
    normals = session.exec(statement).all()
    bouhgts = vendor.bought_items.split(";")

    return vendor_return(
        id=vendor.id,
        name=vendor.name,
        description=vendor.description,
        quote=chosen_quote,
        item_of_the_day=iod,
        normal_items=normals,
        bought_items=bouhgts,
    )
