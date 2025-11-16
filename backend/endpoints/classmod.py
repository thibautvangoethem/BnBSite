from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from rollers.classmodroller import ClassModRoller
from models.classmod import *
from models.common import *
from appglobals import SessionDep
from sqlmodel import select
from models.roll_data import *
from models.rollhistory import RollHistory
from datetime import datetime


router = APIRouter(
    prefix="/classmods",
    tags=["classmods"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/rolldescription", response_model=random_create_description)
def get_create_descritpion(session: SessionDep) -> random_create_description:
    return ClassModRoller.get_roll_description()


@router.post("/generate")
def generate_classmod(
    create_result: random_create_result, session: SessionDep
) -> roll_response:
    newClassMod = ClassModRoller.generate(create_result)
    clm = create_classmod(classmod_data=newClassMod, session=session)
    return roll_response(item_id=clm.id, item_type="classmod")


@router.post("/")
def create_classmod(classmod_data: ClassMod, session: SessionDep) -> ClassMod:
    session.add(classmod_data)
    histoir = RollHistory(
        id=classmod_data.id,
        date=datetime.now(),
        description=str(classmod_data),
        type="Classmod",
    )
    session.add(histoir)
    session.commit()
    session.refresh(classmod_data)

    return classmod_data


@router.put("/{classmod_id}", response_model=ClassMod)
def update_classmod(
    classmod_id: str, classmod: ClassMod, session: SessionDep
) -> ClassMod:
    statement = select(ClassMod).where(ClassMod.id == classmod_id)
    results = session.exec(statement)
    cl_db = results.one()
    cl_db.id = classmod.id
    cl_db.name = classmod.name
    cl_db.description = classmod.description
    cl_db.rarity = classmod.rarity
    cl_db.class_type = classmod.class_type
    cl_db.prefix = classmod.prefix
    cl_db.prefix_effect = classmod.prefix_effect
    cl_db.suffix = classmod.suffix
    cl_db.suffix_effect = classmod.suffix_effect

    session.add(cl_db)
    session.commit()
    session.refresh(cl_db)
    return cl_db


@router.get("/{classmod_id}", response_model=ClassMod)
def get_classmod(classmod_id: str, session: SessionDep) -> ClassMod:
    statement = select(ClassMod).where(ClassMod.id == classmod_id)

    classmod = session.exec(statement).first()

    if classmod is None:
        raise HTTPException(status_code=404, detail="classmod not found")

    return classmod
