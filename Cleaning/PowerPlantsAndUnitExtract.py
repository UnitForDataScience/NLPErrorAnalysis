import json

map = dict()
for row in json.loads(open("./powerPlantUnits.json", "r").read()):
    key = ""
    value = 0
    for possibleString in row[0].split(" "):
        if not possibleString.isnumeric():
            key = key + " " + possibleString
    if key in map:
        map[key] = map[key] + 1
    else:
        map[key] = 1

print(map)
