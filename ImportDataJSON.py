"""import json
import os
def importJSON(categories, inputs):
    JSON_DATA = '{}'
    data = json.loads(JSON_DATA)

    for x in range(len(inputs)):
        data[categories[x]] = inputs[x]
        inputs.append(x)

    with open('finalscore_data.json', 'r') as outfile:
        data1 = json.load(outfile)

    data1.append(data)

    with open('finalscore_data.json', 'w') as outfile:
        json.dump(data1, outfile, indent=4)

importJSON(["timer", "name"], ["10", "aeaeaea"])"""
import json
import os

def importJSON(categories, inputs):
    data = {}

    for x in range(len(inputs)):
        data[categories[x]] = inputs[x]

    if not os.path.exists('finalscore_data.json'):
        with open('finalscore_data.json', 'w') as outfile:
            json.dump([], outfile)

    with open('finalscore_data.json', 'r') as outfile:
        try:
            data1 = json.load(outfile)
            if not isinstance(data1, list):
                data1 = [data1]
        except json.JSONDecodeError:
            data1 = []

    data1.append(data)

    with open('finalscore_data.json', 'w') as outfile:
        json.dump(data1, outfile, indent=4)

importJSON(["timer", "name", "score"], ["10", "uwu","69"])
