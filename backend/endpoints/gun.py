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


import uuid

router = APIRouter(
    prefix="/guns",
    tags=["guns"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# custom creation of gun
class GunCreate(SQLModel):
    name: str
    description: Optional[str] = None
    rarity: Rarity
    manufacturer: Manufacturer
    manufacturer_effect: Optional[str] = None
    element: Optional[str] = None
    prefix_ids: List[str] = []
    postfix_ids: List[str] = []
    redtext_ids: List[str] = []

    range: int
    lowNormal: int
    lowCrit: int
    mediumNormal: int
    mediumCrit2: int
    highNormal: int
    highCrit: int


@router.get("/")
def read_guns(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Gun]:
    guns = session.exec(select(Gun).offset(offset).limit(limit)).all()
    return guns


@router.get("/rolldescription", response_model=random_create_description)
def get_create_descritpion(session: SessionDep) -> random_create_description:
    description = random_create_description(
        level=True,
        selections=selection_descriptions(
            mandatory=[
                selection_description(
                    name="favoured_manufacturer",
                    options=[member.value for member in Manufacturer],
                ),
                selection_description(
                    name="favoured_guns",
                    options=[member.value for member in GunType],
                ),
            ],
            optional=[],  # todo optional choice later
        ),
        rolls=[
            roll_description(name="gun1", dice=Dice.D8),
            roll_description(name="gun2", dice=Dice.D8),
            roll_description(name="rarity1", dice=Dice.D4),
            roll_description(name="rarity2", dice=Dice.D6),
            roll_description(name="element", dice=Dice.D100),
            roll_description(name="prefix", dice=Dice.D100),
            roll_description(name="redtext", dice=Dice.D100),
        ],
    )
    return description


@router.get("/{gun_id}", response_model=Gun)
def get_gun(gun_id: str, session: SessionDep) -> Prefix:
    statement = (
        select(Gun)
        .options(selectinload(Gun.prefixes), selectinload(Gun.postfixes))
        .where(Gun.id == gun_id)
    )

    gun = session.exec(statement).first()

    if gun is None:
        raise HTTPException(status_code=404, detail="Gun not found")

    return gun


@router.post("/")
def create_gun(gun_data: GunCreate, session: SessionDep) -> Gun:
    # Create a new Gun instance
    gun = Gun(
        id=str(uuid.uuid4()),
        name=gun_data.name,
        description=gun_data.description,
        rarity=gun_data.rarity,
        manufacturer=gun_data.manufacturer,
        manufacturer_effect=gun_data.manufacturer_effect,
    )

    session.add(gun)
    session.commit()
    session.refresh(gun)

    for prefix_id in gun_data.prefix_ids:
        prefix = session.get(Prefix, prefix_id)
        if prefix:
            gun.prefixes.append(prefix)
        else:
            raise HTTPException(
                status_code=404, detail=f"Prefix with id {prefix_id} not found"
            )

    for postfix_id in gun_data.postfix_ids:
        postfix = session.get(Postfix, postfix_id)
        if postfix:
            gun.postfixes.append(postfix)
        else:
            raise HTTPException(
                status_code=404, detail=f"Postfix with id {postfix_id} not found"
            )

    for redtext_id in gun_data.redtext_ids:
        redtext = session.get(RedText, redtext_id)
        if redtext:
            gun.redtexts.append(redtext)
        else:
            raise HTTPException(
                status_code=404, detail=f"Redtext with id {redtext_id} not found"
            )

    session.commit()
    session.refresh(gun)

    return gun
