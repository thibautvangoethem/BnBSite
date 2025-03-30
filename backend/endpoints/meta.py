from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from models.gun import Postfix, Prefix
from appglobals import SessionDep, oauth2_scheme
from sqlmodel import select
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from typing import List


import uuid

router = APIRouter(
    prefix="/meta",
    tags=["meta"],
    responses={404: {"description": "Not found"}},
)


@router.post("/postfixes/", response_model=Postfix)
def create_postfix(postfix: Postfix, session: SessionDep) -> Postfix:
    if postfix.id is None:
        postfix.id = str(uuid.uuid4())
    session.add(postfix)
    session.commit()
    session.refresh(postfix)
    return postfix


@router.get("/postfixes/", response_model=List[Postfix])
def get_postfixes(session: SessionDep) -> List[Postfix]:
    postfixes = session.exec(select(Postfix)).all()
    return postfixes


@router.get("/postfixes/{postfix_id}", response_model=Postfix)
def get_postfix(postfix_id: str, session: SessionDep) -> Postfix:
    postfix = session.get(Postfix, postfix_id)
    if postfix is None:
        raise HTTPException(status_code=404, detail="Postfix not found")
    return postfix


@router.post("/prefixes/", response_model=Prefix)
def create_prefix(prefix: Prefix, session: SessionDep) -> Prefix:
    if prefix.id is None:
        prefix.id = str(uuid.uuid4())
    session.add(prefix)
    session.commit()
    session.refresh(prefix)
    return prefix


@router.get("/prefixes/", response_model=List[Prefix])
def get_prefixes(session: SessionDep) -> List[Prefix]:
    prefixes = session.exec(select(Prefix)).all()
    return prefixes


@router.get("/prefixes/{prefix_id}", response_model=Prefix)
def get_prefix(prefix_id: str, session: SessionDep) -> Prefix:
    prefix = session.get(Prefix, prefix_id)
    if prefix is None:
        raise HTTPException(status_code=404, detail="Prefix not found")
    return prefix
