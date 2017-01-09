import json
import unicodedata

data_file = open('concerts.json')
theatres = json.load(data_file)
data_file.close()

data_file = open('events.json')
events = json.load(data_file)
data_file.close()

tmpEvents = {}

for e in events:
    k = unicodedata.normalize('NFKD', e["placeName"]).encode('ascii', 'ignore').decode("utf-8")
    del e["placeName"]

    if (k not in tmpEvents):
        tmpEvents[k] = []

    tmpEvents[k].append(e)

for i in range(0, len(theatres)):
    k = unicodedata.normalize('NFKD', theatres[i]["name"]).encode('ascii', 'ignore').decode("utf-8")

    if (k in tmpEvents):
        theatres[i]["events"] = tmpEvents[k]
    else:
        print(k)

with open('results.json', 'w') as outFile:
    json.dump(theatres, outFile)


#print(data[0]["name"])
