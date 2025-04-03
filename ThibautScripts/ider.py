# kmoest random ids hebben voor alle items

import json
import uuid

f = open(
    "C:\\Users\\thiba\\Desktop\\bnbsite\\BnBSite\\backend\\database_utils\\data\\redtext.json"
)
# print(f.read())
temp = json.load(f)


for i in temp:
    i["id"] = str(uuid.uuid4())

print(json.dumps(temp))
