import json, os

with open('day_ahead.json', 'r') as openfile:
    json_object = json.load(openfile)

print(type(json_object))
print(json.dumps(json_object, indent=2))
print("*" *40)
print(json.dumps(json_object[0]["values"], indent=2))
print("-" *40)
print(json_object[0]["values"][0].keys())
