from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from rollers.grenaderoller import GrenadeRoller
from models.gun import *
from models.common import *
from appglobals import SessionDep
from sqlmodel import select
from models.roll_data import *
from models.grenade import Grenade
from models.rollhistory import RollHistory
from datetime import datetime


router = APIRouter(
    prefix="/grenades",
    tags=["grenade"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/rolldescription", response_model=random_create_description)
def get_create_descritpion(session: SessionDep) -> random_create_description:
    return GrenadeRoller.get_roll_description()


@router.get("/{grenade_id}", response_model=Grenade)
def get_grenade(grenade_id: str, session: SessionDep) -> Grenade:
    statement = select(Grenade).where(Grenade.id == grenade_id)

    grenade = session.exec(statement).first()

    if grenade is None:
        raise HTTPException(status_code=404, detail="grenade not found")

    return grenade


@router.post("/generate")
def generate_grenade(
    create_result: random_create_result, session: SessionDep
) -> roll_response:

    newgrande = GrenadeRoller.generate(create_result)
    gren = create_grenade(grenade_data=newgrande, session=session)
    return roll_response(item_id=gren.id, item_type="grenade")


@router.post("/")
def create_grenade(grenade_data: Grenade, session: SessionDep) -> Grenade:
    session.add(grenade_data)
    histoir = RollHistory(
        id=grenade_data.id,
        date=datetime.now(),
        description=str(grenade_data),
        type="Grenade",
    )
    session.add(histoir)
    session.commit()
    session.refresh(grenade_data)

    return grenade_data


@router.put("/{grenade_id}", response_model=Grenade)
def update_grenade(grenade_id: str, grenade: Grenade, session: SessionDep) -> Grenade:
    statement = select(Grenade).where(Grenade.id == grenade_id)
    results = session.exec(statement)
    grenade_db = results.one()
    grenade_db.id = grenade.id
    grenade_db.name = grenade.name
    grenade_db.description = grenade.description
    grenade_db.rarity = grenade.rarity
    grenade_db.manufacturer = grenade.manufacturer
    grenade_db.manufacturer_effect = grenade.manufacturer_effect
    grenade_db.primer_effect = grenade.primer_effect
    grenade_db.detonater_effect = grenade.detonater_effect
    grenade_db.red_text_name = grenade.red_text_name
    grenade_db.red_text_description = grenade.red_text_description
    grenade_db.damage = grenade.damage
    grenade_db.radius = grenade.radius

    session.add(grenade_db)
    session.commit()
    session.refresh(grenade_db)
    return grenade_db
