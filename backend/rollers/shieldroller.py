import json
import math
import random
from uuid import uuid4
import uuid
from models.shield import Shield
from models.potion import PotionCreate
from rollers.roller import Roller
from models.common import (
    Dice,
    Rarity,
)
from models.roll_data import *

manufacturer_to_number = {
    "ANSHIN": 0,
    "PANGOLIN": 1,
    "HYPERION": 2,
    "TORGUE": 3,
    "VLADOFF": 4,
    "BANDIT": 5,
    "MALIWAN": 6,
    "TEDIORE": 7,
}

shield_rarities_data = [
    {"name": "COMMON", "range": [1, 40]},
    {"name": "UNCOMMON", "range": [41, 70]},
    {"name": "RARE", "range": [71, 85]},
    {"name": "EPIC", "range": [86, 95]},
    {"name": "LEGENDARY", "range": [96, 100]},
]

base_values = [
    {"Level": [1, 5], "Capacity": 100, "RechargeRate": 12},
    {"Level": [6, 11], "Capacity": 250, "RechargeRate": 18},
    {"Level": [12, 17], "Capacity": 500, "RechargeRate": 25},
    {"Level": [18, 23], "Capacity": 900, "RechargeRate": 33},
    {"Level": [24, 29], "Capacity": 1400, "RechargeRate": 42},
    {"Level": [30, 35], "Capacity": 2000, "RechargeRate": 52},
    {"Level": [36, 41], "Capacity": 2800, "RechargeRate": 63},
    {"Level": [42, 47], "Capacity": 3700, "RechargeRate": 75},
    {"Level": [48, 49], "Capacity": 4800, "RechargeRate": 88},
    {"Level": [50], "Capacity": 5500, "RechargeRate": 100},
]

manifacturer_data = [
    {
        "name": "ANSHIN",
        "effects": {
            "COMMON": {
                "capacity_modifier": -20,
                "recharge_rate_modifier": 0,
                "recharge_delay_modifier": 0,
                "stat_modifiers": [{"stat": "health_regen", "amount": 20}],
                "special_effects": [],
                "scales_with_level": False,
            },
            "UNCOMMON": {
                "capacity_modifier": -20,
                "stat_modifiers": [{"stat": "health_regen", "amount": 20}],
                "special_effects": [
                    "Immunity to last received status effect for next 2 turns"
                ],
            },
            "RARE": {
                "capacity_modifier": -20,
                "stat_modifiers": [{"stat": "health_regen", "amount": 30}],
                "special_effects": [
                    "Immunity to last received status effect for next 2 turns"
                ],
            },
            "EPIC": {
                "capacity_modifier": -20,
                "stat_modifiers": [{"stat": "health_regen", "amount": 40}],
                "special_effects": [
                    "Immunity to last received status effect for next 5 turns"
                ],
            },
            "LEGENDARY": {
                "capacity_modifier": 0,
                "stat_modifiers": [{"stat": "health_regen", "amount": 50}],
                "special_effects": [
                    "Immunity to last received status effect for next 5 turns"
                ],
            },
        },
    },
    {
        "name": "PANGOLIN",
        "effects": {
            "COMMON": {
                "capacity_modifier": 30,
                "recharge_delay_modifier": 0,
                "special_effects": ["-2 movement during full shields"],
            },
            "UNCOMMON": {
                "capacity_modifier": 40,
                "special_effects": ["-1 movement during full shields"],
            },
            "RARE": {
                "capacity_modifier": 60,
                "special_effects": ["-1 movement during full shields"],
            },
            "EPIC": {"capacity_modifier": 60, "special_effects": []},
            "LEGENDARY": {
                "capacity_modifier": 100,
                "special_effects": ["+1 movement during full shields"],
            },
        },
    },
    {
        "name": "HYPERION",
        "effects": {
            "COMMON": {
                "capacity_modifier": 0,
                "special_effects": [
                    "Amp shot: consume 10% shields to do 10% more damage"
                ],
            },
            "UNCOMMON": {
                "special_effects": [
                    "Amp shot: consume 20% shields to do 30% more damage"
                ]
            },
            "RARE": {
                "special_effects": [
                    "Amp shot: consume 20% shields to do 50% more damage"
                ]
            },
            "EPIC": {
                "special_effects": [
                    "Amp shot: consume 40% shields to do 100% more damage"
                ]
            },
            "LEGENDARY": {
                "special_effects": [
                    "Amp shot: consume 0% shields to do 100% more damage"
                ]
            },
        },
    },
    {
        "name": "TORGUE",
        "effects": {
            "COMMON": {
                "capacity_modifier": -10,
                "recharge_rate_modifier": -20,
                "special_effects": ["3x3 nova damage on shield depletion"],
                "scales_with_level": True,
            },
            "UNCOMMON": {
                "recharge_rate_modifier": -20,
                "special_effects": ["3x3 nova damage on shield depletion"],
                "scales_with_level": True,
            },
            "RARE": {
                "recharge_rate_modifier": -10,
                "special_effects": ["3x3 nova damage on shield depletion"],
                "scales_with_level": True,
            },
            "EPIC": {
                "recharge_rate_modifier": -10,
                "special_effects": ["4x4 nova damage on shield depletion"],
                "scales_with_level": True,
            },
            "LEGENDARY": {
                "recharge_rate_modifier": 10,
                "special_effects": ["5x5 nova damage on shield depletion"],
                "scales_with_level": True,
            },
        },
    },
    {
        "name": "VLADOFF",
        "effects": {
            "COMMON": {
                "special_effects": [
                    "1% chance to absorb enemy hit and add damage to shields"
                ],
                "cooldown": "3 turns",
            },
            "UNCOMMON": {
                "special_effects": [
                    "5% chance to absorb enemy hit and add damage to shields"
                ],
                "cooldown": "3 turns",
            },
            "RARE": {
                "special_effects": [
                    "10% chance to absorb enemy hit and add damage to shields"
                ],
                "cooldown": "3 turns",
            },
            "EPIC": {
                "special_effects": [
                    "20% chance to absorb enemy hit and add damage to shields"
                ],
                "cooldown": "3 turns",
            },
            "LEGENDARY": {
                "special_effects": [
                    "35% chance to absorb enemy hit and add damage to shields"
                ],
                "cooldown": "2 turns",
            },
        },
    },
    {
        "name": "BANDIT",
        "effects": {
            "COMMON": {
                "recharge_delay_modifier": 100,
                "special_effects": ["+10% extra roid damage while depleted"],
            },
            "UNCOMMON": {
                "recharge_delay_modifier": 150,
                "special_effects": ["+20% extra roid damage while depleted"],
            },
            "RARE": {
                "recharge_delay_modifier": 150,
                "special_effects": ["+30% extra roid damage while depleted"],
            },
            "EPIC": {
                "recharge_delay_modifier": 200,
                "special_effects": ["+50% extra roid damage while depleted"],
            },
            "LEGENDARY": {
                "recharge_delay_modifier": 100,
                "special_effects": ["+100% extra roid damage while depleted"],
            },
        },
    },
    {
        "name": "MALIWAN",
        "effects": {
            "COMMON": {
                "capacity_modifier": -40,
                "special_effects": ["3x3 nova damage on depletion"],
                "element_roll": True,
                "scales_with_level": True,
            },
            "UNCOMMON": {
                "capacity_modifier": -20,
                "special_effects": ["3x3 nova damage on depletion"],
                "element_roll": True,
                "scales_with_level": True,
            },
            "RARE": {
                "capacity_modifier": 0,
                "special_effects": ["3x3 nova damage on depletion"],
                "element_roll": True,
                "scales_with_level": True,
            },
            "EPIC": {
                "capacity_modifier": 10,
                "special_effects": ["3x3 nova damage on depletion"],
                "element_roll": True,
                "scales_with_level": True,
            },
            "LEGENDARY": {
                "capacity_modifier": 25,
                "special_effects": ["3x3 nova damage on depletion"],
                "element_roll": True,
                "scales_with_level": True,
            },
        },
    },
    {
        "name": "TEDIORE",
        "effects": {
            "COMMON": {"capacity_modifier": 10, "special_effects": []},
            "UNCOMMON": {"capacity_modifier": 15, "special_effects": []},
            "RARE": {"capacity_modifier": 20, "special_effects": []},
            "EPIC": {"capacity_modifier": 25, "special_effects": []},
            "LEGENDARY": {
                "capacity_modifier": 25,
                "special_effects": [
                    "On shield depletion, throw a digistructed copy that deals kinetic damage equal to total capacity"
                ],
            },
        },
    },
]


nova_damage_data = [
    {"Level": [1, 6], "damage": "1d12"},
    {"Level": [7, 12], "damage": "2d10"},
    {"Level": [13, 18], "damage": "3d12"},
    {"Level": [19, 24], "damage": "3d20"},
    {"Level": [25, 30], "damage": "5d10"},
    {"Level": [31, 37], "damage": "6d12"},
    {"Level": [38, 44], "damage": "8d10"},
    {"Level": [45, 50], "damage": "10d12"},
]

all_battery_data = [
    {
        "name": "ANSHIN",
        "effects": {
            "COMMON": {
                "special_effects": [
                    "Regain 5% of shields lost when taking elemental damage, once per round"
                ]
            },
            "UNCOMMON": {
                "special_effects": [
                    "Regain 10% of shields lost when taking elemental damage, once per round"
                ]
            },
            "RARE": {
                "special_effects": [
                    "Regain 15% of shields lost when taking elemental damage, once per round"
                ]
            },
            "EPIC": {
                "special_effects": [
                    "Regain 20% of shields lost when taking elemental damage, once per round"
                ]
            },
            "LEGENDARY": {
                "special_effects": [
                    "Regain 25% of shields lost when taking elemental damage, once per round"
                ]
            },
        },
    },
    {
        "name": "PANGOLIN",
        "effects": {
            "COMMON": {"capacity_modifier": 10},
            "UNCOMMON": {"capacity_modifier": 20},
            "RARE": {"capacity_modifier": 30},
            "EPIC": {"capacity_modifier": 40},
            "LEGENDARY": {"capacity_modifier": 50},
        },
    },
    {
        "name": "HYPERION",
        "effects": {
            "COMMON": {"recharge_delay_modifier": -20},
            "UNCOMMON": {"recharge_delay_modifier": -20},
            "RARE": {"recharge_delay_modifier": -20},
            "EPIC": {"recharge_delay_modifier": -20},
            "LEGENDARY": {"recharge_delay_modifier": -20},
        },
    },
    {
        "name": "TORGUE",
        "effects": {
            "COMMON": {"recharge_delay_modifier": 50, "recharge_rate_modifier": 50},
            "UNCOMMON": {"recharge_delay_modifier": 50, "recharge_rate_modifier": 50},
            "RARE": {"recharge_delay_modifier": 50, "recharge_rate_modifier": 50},
            "EPIC": {"recharge_delay_modifier": 50, "recharge_rate_modifier": 50},
            "LEGENDARY": {"recharge_delay_modifier": 50, "recharge_rate_modifier": 50},
        },
    },
    {
        "name": "MALIWAN",
        "effects": {
            "COMMON": {
                "special_effects": [
                    "Gain advantage on status effect checks while shields are up"
                ]
            },
            "UNCOMMON": {
                "special_effects": [
                    "Gain advantage on status effect checks while shields are up"
                ]
            },
            "RARE": {
                "special_effects": [
                    "Gain advantage on status effect checks while shields are up"
                ]
            },
            "EPIC": {
                "special_effects": [
                    "Gain advantage on status effect checks while shields are up"
                ]
            },
            "LEGENDARY": {
                "special_effects": [
                    "Gain advantage on status effect checks while shields are up"
                ]
            },
        },
    },
    {
        "name": "VLADOFF",
        "effects": {
            "COMMON": {
                "special_effects": [
                    "+1 hit on all guns except launchers while shields are up"
                ]
            },
            "UNCOMMON": {
                "special_effects": [
                    "+1 hits on all guns except launchers while shields are up"
                ]
            },
            "RARE": {
                "special_effects": [
                    "+1 hits on all guns except launchers while shields are up"
                ]
            },
            "EPIC": {
                "special_effects": [
                    "+1 hits on all guns except launchers while shields are up"
                ]
            },
            "LEGENDARY": {
                "special_effects": [
                    "+1 hits on all guns except launchers while shields are up"
                ]
            },
        },
    },
    {
        "name": "BANDIT",
        "effects": {
            "COMMON": {
                "special_effects": [
                    "When Shields deplete fully, gain 10 hit points, (excess become temporary hit points) resets on full recharge"
                ]
            },
            "UNCOMMON": {
                "special_effects": [
                    "When Shields deplete fully, gain 10 hit points, (excess become temporary hit points) resets on full recharge"
                ]
            },
            "RARE": {
                "special_effects": [
                    "When Shields deplete fully, gain 10 hit points, (excess become temporary hit points) resets on full recharge"
                ]
            },
            "EPIC": {
                "special_effects": [
                    "When Shields deplete fully, gain 10 hit points, (excess become temporary hit points) resets on full recharge"
                ]
            },
            "LEGENDARY": {
                "special_effects": [
                    "When Shields deplete fully, gain 10 hit points, (excess become temporary hit points) resets on full recharge"
                ]
            },
        },
    },
    {
        "name": "TEDIORE",
        "effects": {
            "COMMON": {
                "special_effects": ["Gain +2 Speed while shields are recharging"]
            },
            "UNCOMMON": {
                "special_effects": ["Gain +3 Speed while shields are recharging"]
            },
            "RARE": {"special_effects": ["Gain +4 Speed while shields are recharging"]},
            "EPIC": {"special_effects": ["Gain +5 Speed while shields are recharging"]},
            "LEGENDARY": {
                "special_effects": ["Gain +6 Speed while shields are recharging"]
            },
        },
    },
]

all_capacitor_data = [
    {
        "name": "ANSHIN",
        "effects": {
            "COMMON": {
                "special_effects": [
                    "While shields are active, gain +5 health regen each round"
                ]
            },
            "UNCOMMON": {
                "special_effects": [
                    "While shields are active, gain +5 health regen each round"
                ]
            },
            "RARE": {
                "special_effects": [
                    "While shields are active, gain +5 health regen each round"
                ]
            },
            "EPIC": {
                "special_effects": [
                    "While shields are active, gain +5 health regen each round"
                ]
            },
            "LEGENDARY": {
                "special_effects": [
                    "While shields are active, gain +5 health regen each round"
                ]
            },
        },
    },
    {
        "name": "PANGOLIN",
        "effects": {
            "COMMON": {"capacity_modifier": 25, "recharge_delay": 100},
            "UNCOMMON": {"capacity_modifier": 25, "recharge_delay": 100},
            "RARE": {"capacity_modifier": 25, "recharge_delay": 100},
            "EPIC": {"capacity_modifier": 25, "recharge_delay": 100},
            "LEGENDARY": {"capacity_modifier": 25, "recharge_delay": 100},
        },
    },
    {
        "name": "HYPERION",
        "effects": {
            "COMMON": {"recharge_rate_modifier": 50, "capacity_modifier": -20},
            "UNCOMMON": {"recharge_rate_modifier": 50, "capacity_modifier": -20},
            "RARE": {"recharge_rate_modifier": 50, "capacity_modifier": -20},
            "EPIC": {"recharge_rate_modifier": 50, "capacity_modifier": -20},
            "LEGENDARY": {"recharge_rate_modifier": 50, "capacity_modifier": -20},
        },
    },
    {
        "name": "TORGUE",
        "effects": {
            "COMMON": {
                "special_effects": [
                    "on full depletion, causes a small shockwave that pushes enemies back 1 square"
                ]
            },
            "UNCOMMON": {
                "special_effects": [
                    "on full depletion, causes a small shockwave that pushes enemies back 1 square"
                ]
            },
            "RARE": {
                "special_effects": [
                    "on full depletion, causes a small shockwave that pushes enemies back 1 square"
                ]
            },
            "EPIC": {
                "special_effects": [
                    "on full depletion, causes a small shockwave that pushes enemies back 1 square"
                ]
            },
            "LEGENDARY": {
                "special_effects": [
                    "on full depletion, causes a small shockwave that pushes enemies back 1 square"
                ]
            },
        },
    },
    {
        "name": "MALIWAN",
        "effects": {
            "COMMON": {"special_effects": ["immune to a random element damage, 1d6"]},
            "UNCOMMON": {"special_effects": ["immune to a random element damage, 1d6"]},
            "RARE": {"special_effects": ["immune to a random element damage, 1d6"]},
            "EPIC": {"special_effects": ["immune to a random element damage, 1d6"]},
            "LEGENDARY": {
                "special_effects": ["immune to a random element damage, 1d6"]
            },
        },
    },
    {
        "name": "VLADOFF",
        "effects": {
            "COMMON": {
                "special_effects": ["while shields are up, +1 square in movement"]
            },
            "UNCOMMON": {
                "special_effects": ["while shields are up, +1 square in movement"]
            },
            "RARE": {
                "special_effects": ["while shields are up, +1 square in movement"]
            },
            "EPIC": {
                "special_effects": ["while shields are up, +1 square in movement"]
            },
            "LEGENDARY": {
                "special_effects": ["while shields are up, +1 square in movement"]
            },
        },
    },
    {
        "name": "BANDIT",
        "effects": {
            "COMMON": {
                "special_effects": [
                    "Shield fully regenerates after 3 rounds of not taking damage"
                ]
            },
            "UNCOMMON": {
                "special_effects": [
                    "Shield fully regenerates after 3 rounds of not taking damage"
                ]
            },
            "RARE": {
                "special_effects": [
                    "Shield fully regenerates after 3 round of not taking damage"
                ]
            },
            "EPIC": {
                "special_effects": [
                    "Shield fully regenerates after 3 round of not taking damage"
                ]
            },
            "LEGENDARY": {
                "special_effects": [
                    "Shield fully regenerates after 3 round of not taking damage"
                ]
            },
        },
    },
    {
        "name": "TEDIORE",
        "effects": {
            "COMMON": {"special_effects": ["on depletion, gain +1d4 to critical hits"]},
            "UNCOMMON": {
                "special_effects": ["on depletion, gain +1d4 to critical hits"]
            },
            "RARE": {"special_effects": ["on depletion, gain +1d4 to critical hits"]},
            "EPIC": {"special_effects": ["on depletion, gain +1d4 to critical hits"]},
            "LEGENDARY": {
                "special_effects": ["on depletion, gain +1d4 to critical hits"]
            },
        },
    },
]

all_red_text_data = [
    {
        "name": "The Floor is Lava",
        "description": "While shields are full, movement speed doubles, but standing still causes 8*player level fire damage.",
    },
    {
        "name": "I'm Rubber, You're Glue",
        "description": "Bullets that hit your shield have a 10% chance to ricochet back at attackers.",
    },
    {
        "name": "This is MY Boomstick!",
        "description": "Shotguns always have full damage when this shield is equipped.",
    },
    {
        "name": "Blink and You\u2019ll Miss It",
        "description": "Briefly gain invisibility for 1 turn when shields start recharging. resets on full charged shields",
    },
    {
        "name": "Can\u2019t Touch This",
        "description": "When you didn\u2019t take damage last round, fully regain shields.",
    },
    {
        "name": "It's a Feature, Not a Bug",
        "description": "Shields randomly overcharge while recharging, doubling capacity for 2 rounds but preventing recharge after.",
    },
    {
        "name": "Static Cling",
        "description": "Nearby enemies suffer 40*shield level Shock DoT while shields are full.",
    },
    {
        "name": "Live to Regret It",
        "description": "Enemies who break your shield take 50% increased damage from all sources.",
    },
    {
        "name": "Gotta Go Fast",
        "description": "Can sacrifice 50% of your max shield capacity to gain 2 extra movements this turn.",
    },
    {
        "name": "Second Skin",
        "capacity_modifier": -50,
        "description": "Once per combat it recharges instantly when fully depleted.",
    },
    {
        "name": "Overkill Protocol",
        "description": "Dealing a critical hit restores a small portion of shields equal to crit damage.",
    },
    {
        "name": "Newton's Third Law",
        "description": "Taking melee damage knocks both you and the attacker back 2 squares.",
    },
    {
        "name": "Cooler Than You",
        "description": "When shield breaks, Cryo nova is applied to nearby enemies at half damage but they get slowed.",
    },
    {
        "name": "Leave Me Alone",
        "description": "While shields are broken, enemies are more likely to attack other targets if in their attack range.",
    },
    {
        "name": "Who Needs Backup?",
        "capacity_modifier": 50,
        "description": "Shield only recharges when no allies are nearby",
    },
    {
        "name": "Bet You Weren\u2019t Expecting That",
        "description": "Each time your shield is depleted, a random status name resistance is gained for 2 rounds.",
    },
    {
        "name": "Just a Flesh Wound",
        "description": "Taking health damage instead of shield damage doubles your total shield recharge speed.",
    },
    {
        "name": "Unstable Core",
        "recharge_rate_modifier": 100,
        "description": "Shield recharge rate is doubled, but it has a random chance while charging to discharge and reset to zero, dealing a shock nova damage around you in 3x3.",
    },
    {
        "name": "I Can Do This All Day",
        "description": "Blocking melee attacks reduces half the damage.",
    },
    {
        "name": "I could beat off 100 men",
        "capacity_modifier": -50,
        "recharge_delay_modifier": -100,
        "recharge_rate_modifier": 300,
        "description": "Each time your shield is depleted you get +1 melee attack per turn, this effect can stack",
    },
]


class ShieldRoller(Roller):
    @staticmethod
    def get_roll_description() -> random_create_description:
        return random_create_description(
            level=True,
            selections=selection_descriptions(
                mandatory=[],
                optional=[
                    selection_description(
                        label="rarity",
                        options=[member.value for member in Rarity],
                    ),
                    selection_description(
                        label="enforce_manufacturer",
                        # lol dat zijn niet de bnb manufacturers
                        options=[
                            "ANSHIN",
                            "PANGOLIN",
                            "HYPERION",
                            "TORGUE",
                            "VLADOFF",
                            "BANDIT",
                            "MALIWAN",
                            "TEDIORE",
                        ],
                    ),
                ],  # todo optional choice later
            ),
            rolls=rollswrapper(
                entries=[
                    roll_description(label="Rarity roll", diceList=[Dice.D100]),
                    roll_description(label="Manufacturer", diceList=[Dice.D8]),
                    roll_description(label="Capacitor", diceList=[Dice.D8]),
                    roll_description(label="Baterry", diceList=[Dice.D8]),
                    roll_description(label="Redtext", diceList=[Dice.D20]),
                ],
                uuid=str(uuid4()),
            ),
        )

    @staticmethod
    def generate(create_result: random_create_result) -> PotionCreate:
        level = create_result.level
        recharge_delay = 1

        for value in base_values:
            if value["Level"][0] <= level and level <= value["Level"][-1]:
                capacity = value["Capacity"]
                print(f"CAPACITY {capacity}")
                recharge_rate = value["RechargeRate"]
                print(f"RATE {recharge_rate}")
                break

        for entry in shield_rarities_data:
            roll = create_result.get_roll_for_label("Rarity roll")[0]
            if entry["range"][0] <= roll and roll <= entry["range"][1]:
                rarity = entry["name"]
        rarity_choice = create_result.get_option_for_label("rarity")
        if not (rarity_choice == None or len(rarity_choice) == 0):
            rarity = rarity_choice[0].upper()

        nova_damage = None
        nova_element = None
        roll = create_result.get_roll_for_label("Manufacturer")

        manufacturer_choice = create_result.get_option_for_label("enforce_manufacturer")
        if not (manufacturer_choice == None or len(manufacturer_choice) == 0):
            # yup de roll data aanpassen is hier de properste optie
            roll[0] = manufacturer_to_number[manufacturer_choice[0]] + 1

        manufacturer = manifacturer_data[roll[0] - 1]["name"]
        manufacturer_effect_data = manifacturer_data[roll[0] - 1]["effects"][rarity]

        if cap_mod := manufacturer_effect_data.get("capacity_modifier"):
            capacity = capacity * (1 + (cap_mod / 100))

        if rate_mod := manufacturer_effect_data.get("recharge_rate_modifier"):
            recharge_rate = recharge_rate * (1 + (rate_mod / 100))

        if delay_mod := manufacturer_effect_data.get("recharge_delay_modifier"):
            recharge_rate = recharge_rate * (1 + (delay_mod / 100))

        manufacturer_effect = manufacturer_effect_data.get("special_effects")
        if manufacturer_effect:
            manufacturer_effect = manufacturer_effect[0]
        if manufacturer_effect == []:
            manufacturer_effect = None

        if manufacturer_effect_data.get("scales_with_level"):
            if manufacturer_effect_data.get("element_roll"):
                elemental_rolls = [
                    "fire",
                    "shock",
                    "corrosive",
                    "cryo",
                    "radiation",
                    "choose",
                ]
                nova_element = elemental_rolls[random.randint(0, 5)]
            for value in nova_damage_data:
                if value["Level"][0] <= level and level <= value["Level"][-1]:
                    nova_damage = value["damage"]
                    break

        roll = create_result.get_roll_for_label("Baterry")[0]
        battery = all_battery_data[roll - 1]
        battery_rarity_data = battery["effects"][rarity]

        if cap_mod := battery_rarity_data.get("capacity_modifier"):
            capacity = capacity * (1 + (cap_mod / 100))

        if rate_mod := battery_rarity_data.get("recharge_rate_modifier"):
            recharge_rate = recharge_rate * (1 + (rate_mod / 100))

        if delay_mod := battery_rarity_data.get("recharge_delay_modifier"):
            recharge_rate = recharge_rate * (1 + (delay_mod / 100))

        # TODO needs to work to cast to string instead of list
        battery_effect = battery_rarity_data.get("special_effects")
        if battery_effect:
            battery_effect = battery_effect[0]

        roll = create_result.get_roll_for_label("Capacitor")[0]
        capacitor = all_capacitor_data[roll - 1]
        capacitor_rarity_data = capacitor["effects"][rarity]

        if cap_mod := capacitor_rarity_data.get("capacity_modifier"):
            capacity = capacity * (1 + (cap_mod / 100))

        if rate_mod := capacitor_rarity_data.get("recharge_rate_modifier"):
            recharge_rate = recharge_rate * (1 + (rate_mod / 100))

        if delay_mod := capacitor_rarity_data.get("recharge_delay_modifier"):
            recharge_rate = recharge_rate * (1 + (delay_mod / 100))

        capacitor_effect = capacitor_rarity_data.get("special_effects")
        if capacitor_effect:
            capacitor_effect = capacitor_effect[0]

        red_text_name = None
        red_text_description = None
        if create_result.get_roll_for_label("Rarity roll")[0] >= 96:
            roll = create_result.get_roll_for_label("Redtext")[0]
            red_text_data = all_red_text_data[roll - 1]
            red_text_name = red_text_data["name"]
            red_text_description = red_text_data["description"]

            if cap_mod := red_text_data.get("capacity_modifier"):
                capacity = capacity * (1 + (cap_mod / 100))

            if rate_mod := red_text_data.get("recharge_rate_modifier"):
                recharge_rate = recharge_rate * (1 + (rate_mod / 100))

            if delay_mod := red_text_data.get("recharge_delay_modifier"):
                recharge_rate = recharge_rate * (1 + (delay_mod / 100))

        return Shield(
            id=str(uuid.uuid4()),
            rarity=rarity,
            manufacturer=manufacturer,
            capacity=int(capacity),
            recharge_rate=int(recharge_rate),
            recharge_delay=int(recharge_delay),
            manufacturer_effect=manufacturer_effect,
            battery_effect=battery_effect,
            capacitor_effect=capacitor_effect,
            red_text_name=red_text_name,
            red_text_description=red_text_description,
            nova_damage=nova_damage,
            nova_element=nova_element,
        )
