import json

def importJSON(categories,inputs) :
    JSON_DATA= '{}'
    data = json.loads(JSON_DATA)
    for x in range (len(categories)):
        data[categories[x]]=inputs[x]
    with open('finalscore_data.json', 'w') as outfile:
        json.dump(data, outfile)
