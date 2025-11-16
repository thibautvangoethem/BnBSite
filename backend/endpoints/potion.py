from datetime import datetime
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from rollers.potionroller import PotionRoller
from models.rollhistory import RollHistory
from models.gun import *
from models.common import *
from appglobals import SessionDep
from sqlmodel import select
from models.roll_data import *
from models.potion import *


import uuid

router = APIRouter(
    prefix="/potions",
    tags=["potion"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/rolldescription", response_model=random_create_description)
def get_create_descritpion(session: SessionDep) -> random_create_description:
    return PotionRoller.get_roll_description()


@router.get("/{potion_id}", response_model=Potion)
def get_potion(potion_id: str, session: SessionDep) -> Potion:
    statement = select(Potion).where(Potion.id == potion_id)

    potion = session.exec(statement).first()

    if potion is None:
        raise HTTPException(status_code=404, detail="potion not found")

    return potion


@router.post("/generate")
def generate_potion(
    create_result: random_create_result, session: SessionDep
) -> roll_response:

    pot: Potion = create_potion(PotionRoller.generate(create_result), session=session)
    return roll_response(item_id=pot.id, item_type="potion")


@router.post("/")
def create_potion(potion_data: PotionCreate, session: SessionDep) -> Potion:
    pot = Potion(id=str(uuid.uuid4()), name=potion_data.name, text=potion_data.text)
    session.add(pot)
    histoir = RollHistory(
        id=pot.id, date=datetime.now(), description=str(pot), type="Potion"
    )
    session.add(histoir)
    session.commit()
    session.refresh(pot)
    return pot


class Potionupdate(BaseModel):
    name: str
    text: str
    id: str


@router.put("/{potion_id}", response_model=Potion)
def update_potion(potion_id: str, potion: Potionupdate, session: SessionDep) -> Potion:
    statement = select(Potion).where(Potion.id == potion_id)
    results = session.exec(statement)
    pot = results.one()
    pot.id = potion.id
    pot.name = potion.name
    pot.text = potion.text
    session.add(pot)
    session.commit()
    session.refresh(pot)
    return pot
