from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager

import logging
from fastapi.middleware.cors import CORSMiddleware
import os
import json

from endpoints import (
    authentication,
    hero,
    gun,
    shield,
    grenade,
    potion,
    mobs,
    rollhistory,
    classmod,
)
from appglobals import engine
from database_utils.create_tables import load_prefab_data

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


def create_db_and_tables():
    # create tables if they didnt exist yet, note wont recreate tables on model change
    SQLModel.metadata.create_all(engine)
    load_prefab_data(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# railway doesnt have easy restart options, so will literally make the health check fail if one is needed
health_status = {"status": "healthy"}


@app.get("/health")
async def health_check():
    return health_status


@app.post("/health/fail")
async def fail_health_check():
    global health_status
    health_status = {"status": "unhealthy"}
    return health_status


app.include_router(authentication.router)
app.include_router(hero.router)
app.include_router(gun.router)
app.include_router(shield.router)
app.include_router(grenade.router)
app.include_router(potion.router)
app.include_router(mobs.router)
app.include_router(rollhistory.router)
app.include_router(classmod.router)


app = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
