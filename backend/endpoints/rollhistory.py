# import math
# from typing import List
# from fastapi import APIRouter
# from fastapi import Depends, HTTPException, status, Query
# from fastapi.security import OAuth2PasswordBearer
# from models.rollhistory import RollHistory
# from models.common import *
# from appglobals import SessionDep, oauth2_scheme
# from sqlmodel import select
# from sqlalchemy.orm import selectinload
# from models.roll_data import *
# from models.potion import *
# from uuid import uuid4


# import uuid

# router = APIRouter(
#     prefix="/rollhistory",
#     tags=["rollhistory"],
#     responses={404: {"description": "Not found"}},
# )
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @router.get("/last/{count}", response_model=List[RollHistory])
# def get_last_roll_history(count: int, session: SessionDep) -> random_create_description:
#     statement = select(RollHistory).order_by(RollHistory.date.desc()).limit(count).all()
#     roll_history = session.exec(statement)

#     if not roll_history:
#         raise HTTPException(status_code=404, detail="No roll history found")

#     return roll_history
