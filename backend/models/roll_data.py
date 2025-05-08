from pydantic import BaseModel
from typing import Optional
from models.common import Dice


class roll_description(BaseModel):
    label: str
    diceList: list[Dice]


class selection_description(BaseModel):
    label: str
    options: list[str]


# uuid used for funny hack to trigger front end rerenders rerolling dices
class rollswrapper(BaseModel):
    entries: list[roll_description]
    uuid: str


class selection_descriptions(BaseModel):
    mandatory: list[selection_description]
    optional: list[selection_description]


## main class for describing a roll (given to front end)
class random_create_description(BaseModel):
    level: bool
    selections: selection_descriptions
    rolls: rollswrapper


#### ^ roll description
#### fancy divider which should really be seperate class
#### v roll execution


class selection_choice(BaseModel):
    label: str
    choices: Optional[list[str]]


class roll_result(BaseModel):
    label: str
    # I assume the dice type is correct, I have probably assumed incorrectly
    result: list[int]


## main class that contains the full result of a roll (returned from frontend)
class random_create_result(BaseModel):
    level: int
    selections: list[selection_choice]
    rolls: list[roll_result]

    def get_roll_for_label(self, label: str):
        for roll in self.rolls:
            if roll.label == label:
                return roll.result

    def get_selection_for_label(self, label: str):
        for sel in self.selections:
            if sel.label == label:
                return sel.choices


# def combine_roles(results: list[int]) -> list[int]:
# result_str = []
# for item in results:
#     result_str.append (str(item)

# return int(result_str)


def get_roll_for_label(rolls: list[roll_result], label: str):
    for roll in rolls:
        if roll.label == label:
            return roll.result


def get_selection_for_label(selections: list[roll_result], label: str):
    for roll in rolls:
        if roll.label == label:
            return roll.result


class roll_response(BaseModel):
    item_id: str
    item_type: str
