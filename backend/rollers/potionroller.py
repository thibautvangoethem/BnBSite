import math
from uuid import uuid4
from models.potion import PotionCreate
from rollers.roller import Roller
from models.common import (
    Dice,
)
from models.roll_data import *


potionMap = [
    ("Common Tina Potion", "Roll 1d20 for bombass effect [20g]"),
    ("Common Health Potion", "Regens 1d8 Health [20g]"),
    ("Common Shield Potion", "Recharges 1d8 Shield [15g]"),
    ("Check Potion", "+5 to x Check for 1 hour [20g]"),
    ("Element Potion", "Protection from x Element for 2 turns [15g]"),
    ("Rare Tina Potion", "Roll 1d20+3 for bombass effect [40g]"),
    ("Rare Health Potion", "Regens 2d8+5 Health [40g]"),
    ("Rare Shield Potion", "Recharges 2d8+5 Shield [30g]"),
    ("Stat Potion", "3 to x Stat Mod for 1 hour [40g]"),
    ("Twofer Potion", "Gain 1d8+3 Health and Shield [70g]"),
    ("Epic Tina Potion", "Roll 1d20+5 for bombass effect [100g]"),
    ("Epic Health Potion", "Regens 3d8+10 Health [100g]"),
    ("Epic Shield Potion", "Recharges 3d8+10 Shield [90g]"),
    ("Lucky Potion", "Reroll 1 Die per Attack for 2 turns [100g]"),
    ("Invisibility Potion", "Become Cloaked for 3 turns [120g]"),
    ("Legendary Tina Potion", "Roll 1d20+10 for ombass effect [250g]"),
    ("Legendary Health Potion", "Regens 4d8+20 Health [250g]"),
    ("Legendary Shield Potion", "Recharges 4d8+20 Shield [230g]"),
    ("Fumble Potion", "All 1’s rolled become 20’s for 2 hours [250g]"),
    ("Gold Farmer Potion", "+2d6 to all Cache Rolls for 2 hours [270g]"),
]

tina_potions = [
    ("Golden Gulp", "Shhh! It's just pee, don't tell anyone."),
    (
        "Deadly Horrible Potion of Death",
        "Kills you dead in exactly an hour. Can only be cured by drinking a humbo pushups.",
    ),
    (
        "One Liner Juice",
        "After drinking this, everything you do for the next hour has to be followed with a cool punny one liner, or you spasms taking 5 damage.",
    ),
    (
        "Best Drink Ever",
        "The single best thing you ever have or ever will taste, even if you get another one of these potions it'll never taste as good as the first, so you're sorta bummed forever that nothing tastes as good. This behaves like a permanent trauma.",
    ),
    (
        "What If We Were Girlfriends",
        "The next two people to drink this juice see what their life would be like if they moved their beds together.",
    ),
    (
        "Gotta Sing",
        "You have to sing everything you say for the next hour or until the BM gets bored.",
    ),
    (
        "Friday Freak",
        "The next two people to drink this swap bodies for the rest of the session.",
    ),
    (
        "Love Potion Number 69 (nice)",
        "When you drink this potion, the next person you smooch will love you for exactly sixty-nine (real life) seconds. Once the 69 seconds are up, they'll hate you with the exact same ferocity with which they just loved you.",
    ),
    ("Truth Serum", "You can only tell the truth for the rest of the session."),
    (
        "No Curses Piz",
        "If the drinker curses anytime for the rest of the session, they take 5 damage.",
    ),
    (
        "Gotta Dance",
        "You can't stop dancing for ten minutes. When taking movement actions, describe what sick steps you put down.",
    ),
    (
        "Big Booty Potion",
        "Makes the booty grow 300%. Too juicy. I die. Have fun making up an effect for this, BM.",
    ),
    (
        "Vommodrink",
        "Makes you vomit real bad for thirty seconds. Create a Corrosive puddle in all adjacent squares every turn for however long the BM hates you.",
    ),
    (
        "Stank Drink",
        "Anyone who drinks this smells so bad that people gotta get as far away from them as possible for a half hour. Allies cannot move through any squares within a range of 2 around you.",
    ),
    (
        "Do U Feel Lucky",
        "Has a fifty-fifty chance to give or to drinker 20 HP or deal 20 health damage.",
    ),
    (
        "Bullet Burp",
        "For twenty minutes, you burp uncontrollably, causing bullets to come out and do 1d4 damage each to anyone adjacent. Do NOT kiss anyone after drinking this.",
    ),
    (
        "Buddie Juice",
        "You immediately take the form of the one person you hate the most and wear it off after an hour.",
    ),
    (
        "Do You Like Me Y/N",
        "Anyone drinking this has to tell their true feelings about the BM.",
    ),
    (
        "Roshambo",
        "Exactly once, instead of doing a proper combat against an enemy, you can play rock-paper-scissors with the BM. If you lose, your character is dead forever or at least gets like 3 trauma.",
    ),
    (
        "Punch Drunk",
        "You have to Melee Attack someone every hour or your heart stops, but your Melee Attacks deal a bonus 1d12 damage.",
    ),
    (
        "Butt Farts",
        "Once, during the remainder of the session, you have the ability to do a fart so big it does 2d8 damage to everyone in 2 squares range.",
    ),
    (
        "Haterade",
        "Anyone who drinks this makes everyone around them so mad that they gotta beat the piss out of them for at least a half hour. All enemies make their next Attack against you, probably.",
    ),
    ("Fancy Feast", "Gives you a fancy voice for an hour +10 to Impression Check."),
    (
        "2 Sexy",
        "Makes you reevaluate alluring to one type of creature of the BM's choice. Gain +5 on Talk and interact checks for that enemy type.",
    ),
    (
        "Parent Trap",
        "Whoever drinks this will instantly create a baby with the next person they smooch. The baby will just pop into existence outta thin air.",
    ),
    (
        "Scrappy",
        "Drinkin this gives you a little sidekick who looks like a smaller version of you. They're real irritating but they give you an extra Action every turn and they love you, but they have 1 HP. You or the BM control them and do their voice, whoever wants to.",
    ),
    (
        "Not Today",
        "The next time you would die... you don't. Ignore the would-kill-you damage and get your life together.",
    ),
    ("Liquid Confidence", "Adjacent allies gain +2 to all checks."),
    ("Good Touch", "Your Melee Attacks heal targets."),
    (
        "Tina Tincture",
        "Makes you sound like Tiny Tina, your main man control one non-Boss enemy during the next encounter.",
    ),
]


class PotionRoller(Roller):
    @staticmethod
    def get_roll_description() -> random_create_description:
        return random_create_description(
            level=False,
            selections=selection_descriptions(
                mandatory=[],
                optional=[],  # todo optional choice later
            ),
            rolls=rollswrapper(
                entries=[
                    roll_description(label="Base roll", diceList=[Dice.D100]),
                    roll_description(label="Tina roll", diceList=[Dice.D20]),
                ],
                uuid=str(uuid4()),
            ),
        )

    @staticmethod
    def generate(create_result: random_create_result) -> PotionCreate:
        base_roll = create_result.get_roll_for_label("Base roll")[0]

        index = math.floor((base_roll - 1) / 5)

        result = potionMap[index]
        pot: PotionCreate = PotionCreate(name=result[0], text=result[1])
        if index in [0, 5, 10, 15]:
            tina_roll = create_result.get_roll_for_label("Tina roll")[0]
            match index:
                case 0:
                    pass
                case 5:
                    tina_roll = tina_roll + 3
                case 10:
                    tina_roll = tina_roll + 5
                case 15:
                    tina_roll = tina_roll + 10
                case _:
                    print("thibaut heeft weer liggen koken met de code")
            result = tina_potions[min(tina_roll, len(tina_potions) - 1)]
            return PotionCreate(
                name=f"Tina potion numero {tina_roll}",
                text=result[0] + ": " + result[1],
            )
