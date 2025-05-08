import json


def update_ids(json_data):
    # Iterate over the list and update the 'id' field
    for index, item in enumerate(json_data):
        item["id"] = index + 1
    return json_data


# Example usage
json_input = """
[
    {
        "id": "b64af769-93ed-4814-a98f-5a49b5f165ea",
        "name": "POP POP!",
        "effect": "Deals Crit Damage twice."
    },
    {
        "id": "b62ef4f1-11ce-4383-bf3e-64d75f9ce20e",
        "name": "I never freeze",
        "effect": "Adds Cryo Element type."
    },
    {
        "id": "f42a8846-c3e4-45f2-a932-06a0b5d8f8ef",
        "name": "Toasty!",
        "effect": "Adds Incendiary Element type."
    },
    {
        "id": "a0727cb0-6619-4b44-bb96-1cef39475e97",
        "name": "Was he slow?",
        "effect": "Fires backwards."
    },
    {
        "id": "9240f083-a09f-41c6-97fb-d7f6b632fcb2",
        "name": "We Hate You, Please Die.",
        "effect": "Taunts the farthest Enemy each turn."
    },
    {
        "id": "c7b3736a-12de-4867-a9a1-e72479d82494",
        "name": "Tell them they\u00e2\u20ac\u2122re next",
        "effect": "Won\u00e2\u20ac\u2122t deal Damage to the final Enemy in an encounter."
    },
    {
        "id": "7648cb00-76dc-414c-919a-b5ec611b36eb",
        "name": "PAN SHOT!",
        "effect": "Always Hits the closest Enemy."
    },
    {
        "id": "61a1b9a1-d800-487d-8f6c-cc898307978d",
        "name": "Envision Wyverns",
        "effect": "Adds Radiation Element type."
    },
    {
        "id": "bdef0a07-628d-4ef7-932e-a8c263e88c45",
        "name": "I\u00e2\u20ac\u2122m melting!",
        "effect": "Adds Corrosive Element type."
    },
    {
        "id": "d5a2f472-4f7c-46ef-9675-35950e8fb880",
        "name": "The same thing that happens to everything else.",
        "effect": "Adds Shock Element type."
    },
    {
        "id": "a513f387-b208-4bee-961c-344a40a22b72",
        "name": "360 quickscope",
        "effect": "Adds a Crit to each Ranged Attack."
    },
    {
        "id": "ede5d349-63fb-43d6-bc6d-61db514b61f2",
        "name": "Any Questions?",
        "effect": "Shoots pumpkin bombs that deal an extra 3d6 Explosive Damage."
    },
    {
        "id": "bf6f2bb7-8a2d-443b-b9e4-14e608d520e8",
        "name": "Blood and Thunder",
        "effect": "Take 1d6 Health Damage to deal +3d6 Shock Damage."
    },
    {
        "id": "6162b0a5-155a-4e6c-a667-a77ffc4a7ea7",
        "name": "SI VIS PACEM, PARA BELLUM",
        "effect": "Gain Extra Attack if Acting Before Enemies."
    },
    {
        "id": "345dae07-281e-48e7-9c24-7474ce7d8ae0",
        "name": "You're breathtaking!",
        "effect": "Wielder cannot be targeted on the first turn of an encounter."
    },
    {
        "id": "48bee248-c16c-4614-a6e6-c0a159a56712",
        "name": "Pass turn.",
        "effect": "Wielder may Throw a grenade during the End of Turn step."
    },
    {
        "id": "6aae7158-86ef-4d24-b8be-169e0506cd7e",
        "name": "I am Vengeance!",
        "effect": "Deals 2x Damage to Enemies adjacent to allies."
    },
    {
        "id": "f86073cf-b40d-4a16-98e9-3144c0ab7b76",
        "name": "Roll the dice",
        "effect": "If Accuracy Roll is even, 2x Damage. If Accuracy Roll is odd, half Damage."
    },
    {
        "id": "bfe2af01-7d16-4c94-ac67-bbd7a4699413",
        "name": "One among the fence",
        "effect": "Add 21 Damage if you roll 13+ on your Accuracy Roll. (1/day)"
    },
    {
        "id": "6334b542-5d19-4871-b346-b74feaaa29b6",
        "name": "Don\u00e2\u20ac\u2122t be sorry. Be better.",
        "effect": "Reroll the Badass Die once per day."
    },
    {
        "id": "3bcc16d2-4646-45fa-a3ab-ee3f518a816f",
        "name": "THE PICKLES!",
        "effect": "Shoots flaming cheeseburgers that deal an extra 2d6 Incendiary Damage."
    },
    {
        "id": "cbdd7e6f-69a3-4f46-b96a-1efaba216ca4",
        "name": "Do a kickflip!",
        "effect": "+4 on Traverse Checks while equipped."
    },
    {
        "id": "fc4dae48-d482-4a94-819e-268bef407a05",
        "name": "Extinction is the Rule",
        "effect": "Teleport to any square up to 4 away when you kill an Enemy."
    },
    {
        "id": "f092f6e8-dd49-4847-ac27-56ae5bafbd0b",
        "name": "Never Fight a Knight with a Perm",
        "effect": "DMG Mod +6 against non-human Enemies."
    },
    {
        "id": "9f03672c-f435-4089-b6f5-75631088e51b",
        "name": "Bye bye, little Butt Stallion!",
        "effect": "Shots explode into rainbows that deal an extra 1d8 Damage."
    },
    {
        "id": "050fbd2a-70b7-4745-b30a-8672cdbf5fd0",
        "name": "Time 2 Hack",
        "effect": "+4 on Interact Checks and Melee Damage while equipped."
    },
    {
        "id": "b7a376ed-1cef-4aa7-9365-e58e00befccb",
        "name": "HATE Magic...",
        "effect": "so much +3 DMG Mod. Take 2d6 Vomit Damage if Reloaded."
    },
    {
        "id": "b29130cc-dc38-4f88-987f-7fa4f87ea7c0",
        "name": "OFF WITH THEIR HEADS!",
        "effect": "Roll %s. 95%+: the Enemy's head falls off."
    },
    {
        "id": "57fcce14-c1f9-4e02-a984-88089d25d663",
        "name": "This is my BOOMSTICK!",
        "effect": "Deals 3x Damage to skeletons."
    },
    {
        "id": "641b694a-e048-4154-bca5-7a99ace8cfe0",
        "name": "Super easy, barely an inconvenience",
        "effect": "Automatically pass the first Check each day."
    },
    {
        "id": "7e3eca61-496f-4893-8ffe-f2b9bcf87cba",
        "name": "Hold onto your butts.",
        "effect": "When fired, the wielder and targets Hit are Knocked Back 2 squares."
    },
    {
        "id": "513f64a2-1bcd-4164-a274-5ad7a8a10a12",
        "name": "The Wise Man\u00e2\u20ac\u2122s Fear",
        "effect": "Deals 3x Damage to all wizards."
    },
    {
        "id": "8bf850cc-c8fa-4527-8885-20e03658b17f",
        "name": "I don\u00e2\u20ac\u2122t want this isolation.",
        "effect": "Won\u00e2\u20ac\u2122t fire unless adjacent to an ally or target."
    },
    {
        "id": "a3e9f3d2-1aad-4004-be08-27d4decc87c6",
        "name": "TUFF with two Fs",
        "effect": "Prevents the first 5 Health Damage each turn."
    },
    {
        "id": "3b792767-1bad-4b27-b93a-5c31ad33f7b3",
        "name": "Unlikely Maths",
        "effect": "Roll an extra die of each type rolled during an Attack and take the highest result(s)."
    },
    {
        "id": "5ca74fe5-9ef5-4c3c-bb13-a46b512108bf",
        "name": "Gravity\u00e2\u20ac\u2122s Rainbow",
        "effect": "First Attack against a Badass target always deals max Damage."
    },
    {
        "id": "d5b682a4-78be-4442-9407-647c546d1a74",
        "name": "Let\u00e2\u20ac\u2122s do this one last time...",
        "effect": "Shoots webs that reduce target's Movement to 0 for 1 turn."
    },
    {
        "id": "ace7dcad-126e-459c-994f-b01dfc36cc12",
        "name": "BIP!",
        "effect": "Once per encounter, the wielder can run into squares with an Enemy, Knocking them Back 1 square."
    },
    {
        "id": "a12deec1-928c-4dda-8456-3d73c19d6dd1",
        "name": "The Heaviest Matter of the Universe",
        "effect": "The wielder and targets Hit cannot take Movement Actions while equipped."
    },
    {
        "id": "db59a59e-fcda-4f23-b7ff-2cb149b7284e",
        "name": "GREEN FLAME",
        "effect": "Shoots burst of green flames while firing, dealing 2d6 Incendiary Damage to adjacent targets."
    },
    {
        "id": "c11238e4-3ad0-4e3f-8d40-f59df8363474",
        "name": "More like Bore Ragnarok!",
        "effect": "Gain 1 Badass Token after a successful Talk Check while equipped."
    },
    {
        "id": "3883ee4f-2c55-4a78-856d-0343e2d9196f",
        "name": "That\u00e2\u20ac\u2122s levitation, Holmes!",
        "effect": "Ignore difficult terrain while equipped."
    },
    {
        "id": "ccc82630-1c81-4ce6-a686-1c581fa5c205",
        "name": "Let\u00e2\u20ac\u2122s boo-boo.",
        "effect": "Gain Extra Movement after drinking a potion while equipped."
    },
    {
        "id": "d4ba18a4-46d4-411e-a4f3-1f9068ef9689",
        "name": "Mmm Whatcha Say...",
        "effect": "Gain a Ranged Attack if an Enemy is talking before an encounter."
    },
    {
        "id": "de4b5a22-30e1-41bc-a86e-568bdf70ecb6",
        "name": "Here Comes the FunCooker",
        "effect": "When this gun scores a Crit, the Enemy suffers a miniature combustion, dealing 1d12 Explosive Damage to itself and all adjacent squares."
    },
    {
        "id": "b36963e6-1d8b-4bbb-b157-f724281ea3f5",
        "name": "Overwhelming strength is boring.",
        "effect": "\u00e2\u20ac\u201c6 Initiative. The first non-Badass, non- boss Enemy that is Melee Attacked dies instantly (1/day)."
    },
    {
        "id": "5ffa795b-9577-4de6-a0c1-036ec7bfef02",
        "name": "Stop talking, I will win.",
        "effect": "It\u00e2\u20ac\u2122s what heroes do. Gun fires explosives that deal +3d6 Damage to all adjacent squares."
    },
    {
        "id": "aa6035f1-190f-4722-a573-657e50fe8110",
        "name": "Richer and cleverer than everyone else!",
        "effect": "Add 10 gold per Loot Pile when rolling for Enemy Drops."
    },
    {
        "id": "d3edc7d7-063f-40e9-b77f-3eb4b6886a0a",
        "name": "METAL WILL DESTROY ALL EVIL!",
        "effect": "Allies get +2 ACC Mod each turn you perform a Melee Attack."
    },
    {
        "id": "70ecebef-e27c-4519-9c11-8f7574866c1e",
        "name": "Life is a conundrum of esoterica.",
        "effect": "Gain 2 Badass Tokens the first time you roll for a Trauma each day."
    }
]
"""

# Parse the JSON input
data = json.loads(json_input)

# Update the IDs
updated_data = update_ids(data)

# Print the updated JSON
print(json.dumps(updated_data, indent=4))
