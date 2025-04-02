from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager

import logging
from fastapi.middleware.cors import CORSMiddleware
import os
import json

from endpoints import authentication, hero, gun, meta
from appglobals import engine

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

    # get and upsert default data in model
    datapath = "./backend/models/data/"
    # for model_name, model_class in SQLModel.metadata.tables.items():
    #     json_file_path = datapath + f"{model_name}.json"

    #     # Check if the JSON file exists
    #     if os.path.exists(json_file_path):
    #         # Load default data from JSON file
    #         with open(json_file_path, "r") as file:
    #             default_data = json.load(file)

    #         # Insert default data into the database
    #         with Session(engine) as session:
    #             for record in default_data:
    #                 session.add(model_class(**record))
    #             session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(authentication.router)
app.include_router(hero.router)
app.include_router(gun.router)
app.include_router(meta.router)


app = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
