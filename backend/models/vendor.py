from models.common import Rarity

from sqlmodel import Field, SQLModel


class Vendor(SQLModel, table=True):
    # general metadata
    id: str = Field(primary_key=True)
    name: str = ""
    description: str = None
    quotes: str = ""  # ; delimeted list
    normal_item_amount: int
    supported_items: str  # ; delimeted list
    item_of_the_day_minimum: Rarity

    # data about currently in stock items
    item_of_the_day: str  # a single str id for an item (can query to get info)

    normal_items: str  # multiple ; delimeted ids
    bought_items: str  # multiple ; delimeted ids
