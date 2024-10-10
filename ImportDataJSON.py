import json

def importJSON(categories,inputs) :
    JSON_DATA= '{}'
    data = json.loads(JSON_DATA)
    inputs[10]=1; #in case no difficulty is selected
    for x in range (len(categories)):
        data[categories[x]]=inputs[x]
    # points multiplier depending on the time required
    score = inputs[10]*5*(30-int(inputs[1]))

    with open('finalscore_data.json', 'w') as outfile:
        json.dump(data, outfile)


#points multiplier depending on the time required
categories