from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.classmod import ClassMod
from models.gun import Gun
from models.potion import Potion
from models.shield import Shield
from models.vendor import *
from models.common import *
from appglobals import SessionDep
from sqlmodel import select
from models.roll_data import *
from models.grenade import Grenade
from models.rollhistory import RollHistory
import random

import uuid

router = APIRouter(
    prefix="/vendors",
    tags=["vendors"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class ItemMini(BaseModel):
    id: str
    name: str
    type: str
    description: Optional[str]
    rarity: Optional[Rarity]


class VendorReturn(BaseModel):
    # general metadata
    id: str = Field(primary_key=True)
    name: str = ""
    description: str = None
    quote: str = ""  # single quote chosen

    # data about currently in stock items
    item_of_the_day: ItemMini
    normal_items: list[ItemMini]
    bought_items: list[str]  # multiple ; delimeted ids


def get_item_mini(id: str, session: SessionDep) -> ItemMini:
    item_classes = {
        "gun": Gun,
        "grenade": Grenade,
        "shield": Shield,
        "potion": Potion,
        "classmod": ClassMod,
    }

    statement = select(RollHistory).where(RollHistory.id == id)
    item: RollHistory = session.exec(statement).first()
    item_type = item.type

    if item_type in item_classes:
        # tocheck will the reflection like select still work here even if the id is a reference
        statement = select(item_classes[item_type]).where(
            item_classes[item_type].id == id
        )
        thing = session.exec(statement).first()

        if item_type == "potion":
            return ItemMini(
                id=id,
                name=thing.name,
                type=item_type,
                description=thing.text,
                rarity=None,
            )
        else:
            return ItemMini(
                id=id,
                name=thing.name,
                type=item_type,
                description=thing.description,
                rarity=thing.rarity,
            )


def get_vendor_return(id: str, session: SessionDep) -> VendorReturn:
    statement = select(Vendor).where(Vendor.id == id)
    vendor: Vendor = session.exec(statement).first()

    if vendor is None:
        raise HTTPException(status_code=404, detail="vendor not found")

    chosen_quote = random.choice(vendor.quotes.split(";"))
    iod = get_item_mini(vendor.item_of_the_day)
    normals = [get_item_mini(item) for item in vendor.normal_items.split(";")]
    boughts = vendor.bought_items.split(";")

    return VendorReturn(
        id=vendor.id,
        name=vendor.name,
        description=vendor.description,
        quote=chosen_quote,
        item_of_the_day=iod,
        normal_items=normals,
        bought_items=boughts,
    )


def roll_item(item_type: str) -> RollHistory:
    item_type = item_type.lower()
    if item_type == "gun":
        pass
    elif item_type == "grenade":
        pass
    elif item_type == "shield":
        pass
    elif item_type == "potion":
        pass
    elif item_type == "classmod":
        pass


@router.get("/{vendor_id}/reroll_normal", response_model=VendorReturn)
def rerollvendorNormal(vendor_id: str, session: SessionDep) -> VendorReturn:
    rolled_items = list()

    return get_vendor(vendor_id, session)


@router.get("/{vendor_id}/reroll_iod", response_model=VendorReturn)
def rerollvendoriod(vendor_id: str, session: SessionDep) -> VendorReturn:
    statement = select(Vendor).where(Vendor.id == vendor_id)
    vendor = session.exec(statement).first()
    if vendor is None:
        raise HTTPException(status_code=404, detail="vendor not found")

    temp = vendor.bought_items.split(";")
    temp.remove(vendor.item_of_the_day)
    vendor.bought_items = ";".join(temp)

    chosen_item = random.choice(vendor.supported_items.split(";"))

    return get_vendor(vendor_id, session)


@router.get("/{vendor_id}/buy/{item_id}", response_model=VendorReturn)
def buyitem(vendor_id: str, item_id: str, session: SessionDep) -> VendorReturn:
    statement = select(Vendor).where(Vendor.id == vendor_id)

    vendor = session.exec(statement).first()
    if vendor is None:
        raise HTTPException(status_code=404, detail="vendor not found")
    if not (
        (vendor.item_of_the_day is not None and vendor.item_of_the_day == item_id)
        or (vendor.normal_items is not None and item_id in vendor.normal_items)
    ):
        raise HTTPException(
            status_code=422,
            detail=f"vendor {vendor_id} does not have an item with id {item_id} for sale",
        )

    if item_id in vendor.bought_items:
        raise HTTPException(
            status_code=422,
            detail=f"item {item_id} has already been sold to someone",
        )
    vendor.bought_items += f";{item_id}"

    session.add(vendor)
    session.commit()
    session.refresh(vendor)

    return get_vendor(vendor_id, session)


@router.get("/debug/{vendor_id}", response_model=Vendor)
def get_debug_vendor(vendor_id: str, session: SessionDep) -> Vendor:
    statement = select(Vendor).where(Vendor.id == id)
    vendor: Vendor = session.exec(statement).first()

    if vendor is None:
        raise HTTPException(status_code=404, detail="vendor not found")
    return vendor


@router.get("/{vendor_id}", response_model=VendorReturn)
def get_vendor(vendor_id: str, session: SessionDep) -> VendorReturn:
    return get_vendor_return(id=vendor_id, session=session)


class VendorCreate(BaseModel):
    # general metadata
    name: str = ""
    description: str = None
    quotes: str = ""  # ; delimeted list
    normal_item_amount: int
    supported_items: str  # ; delimeted list
    item_of_the_day_minimum: Rarity


@router.post("/")
def create_vendor(vendor: VendorCreate, session: SessionDep) -> Vendor:
    toadd = Vendor()
    toadd.id = str(uuid.uuid4())
    toadd.description = vendor.description
    toadd.quotes = vendor.quotes
    toadd.normal_item_amount = vendor.normal_item_amount
    toadd.supported_items = vendor.supported_items
    toadd.item_of_the_day_minimum = vendor.item_of_the_day_minimum

    # todo roll the new vendor the first time

    session.add(toadd)
    session.commit()
    session.refresh(vendor)
    return vendor
