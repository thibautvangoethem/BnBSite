from fastapi import APIRouter, UploadFile, File
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from models.gun import Postfix, Prefix, RedText
from appglobals import SessionDep, oauth2_scheme
from sqlmodel import select
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from typing import List
import json


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


@router.post("/postfix_json/")
async def upsert_postfix_endpoint(file: UploadFile, session: SessionDep):
    try:
        contents = await file.read()
        data = json.loads(contents)

        if not isinstance(data, list):
            raise HTTPException(
                status_code=400,
                detail="Invalid JSON format. Expected a list of objects.",
            )

        for item in data:
            session.add(Postfix(**item))
        session.commit()

        return {"message": "Upsert completed successfully"}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@router.post("/prefix_json/")
async def upsert_prefix_endpoint(file: UploadFile, session: SessionDep):
    try:
        contents = await file.read()
        data = json.loads(contents)

        if not isinstance(data, list):
            raise HTTPException(
                status_code=400,
                detail="Invalid JSON format. Expected a list of objects.",
            )

        for item in data:
            session.add(Prefix(**item))
        session.commit()

        return {"message": "Upsert completed successfully"}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/redtexts/", response_model=RedText)
def create_redtext(redtext: RedText, session: SessionDep) -> RedText:
    if redtext.id is None:
        redtext.id = str(uuid.uuid4())
    session.add(redtext)
    session.commit()
    session.refresh(redtext)
    return redtext


@router.get("/redtexts/", response_model=List[RedText])
def get_redtexts(session: SessionDep) -> List[RedText]:
    redtexts = session.exec(select(RedText)).all()
    return redtexts


@router.get("/redtexts/{redtext_id}", response_model=RedText)
def get_redtext(redtext_id: str, session: SessionDep) -> RedText:
    redtext = session.get(RedText, redtext_id)
    if redtext is None:
        raise HTTPException(status_code=404, detail="RedText not found")
    return redtext


@router.post("/redtext_json/")
async def upsert_redtext_endpoint(file: UploadFile, session: SessionDep):
    try:
        contents = await file.read()
        data = json.loads(contents)

        if not isinstance(data, list):
            raise HTTPException(
                status_code=400,
                detail="Invalid JSON format. Expected a list of objects.",
            )

        for item in data:
            session.add(RedText(**item))
        session.commit()

        return {"message": "Upsert completed successfully"}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
