from fastapi import APIRouter
from fastapi import Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from models.hero import Hero
from appglobals import SessionDep, oauth2_scheme
from sqlmodel import select

import uuid

router = APIRouter(
    prefix="/hero",
    tags=["hero"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/testAdd")
def addEntryTest(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
) -> Hero:
    hero = Hero()
    hero.id = str(uuid.uuid4())
    hero.name = str(uuid.uuid4())
    hero.age = 10
    hero.secret_name = str(uuid.uuid4())
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("/testGet")
def getAll(session: SessionDep) -> list[Hero]:
    heroes = session.exec(select(Hero)).all()
    return list(heroes)


@router.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
