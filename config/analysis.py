import json

with open("starters.json") as s:
    start = json.load(s)

with open("history.txt") as _file:
    lines = _file.readlines()

for line in lines:
    starter = line.split(' ', 1)[0]

    if starter in start:
        start[starter] += 1
    else:
        start[starter] = 1

    print(starter[0])

with open ("starters.json", "w") as f:
    json.dump(start, f, indent=4, sort_keys=True) 

