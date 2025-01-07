from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
import uuid
import logging
from fastapi.middleware.cors import CORSMiddleware
import os

LOG = logging.getLogger(__name__)

origins = [
    # "http://localhost",
    "*",
]
if "VITE_FRONTEND_URL" in os.environ:
    # origins.append(str(os.environ["VITE_FRONTEND_URL"]))
    pass
else:
    LOG.info("FAILING")
    LOG.info(str(origins))


class Hero(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


connect_args = {"check_same_thread": False}
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/bnbsite"
if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ["DATABASE_URL"]
else:
    LOG.info("WARNING, DATABASE_URL environ not found, assuming local execution")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)


@app.get("/testAdd")
def test(session: SessionDep) -> Hero:
    hero = Hero()
    hero.id = str(uuid.uuid4())
    hero.name = str(uuid.uuid4())
    hero.age = 10
    hero.secret_name = str(uuid.uuid4())
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.get("/testGet")
def test(session: SessionDep) -> list[Hero]:
    heroes = session.exec(select(Hero)).all()
    return list(heroes)


@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.get("/heroes/")
def read_heroes(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}


app = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == '__main__':
    uvicorn.run(app, host=None, port=8000)