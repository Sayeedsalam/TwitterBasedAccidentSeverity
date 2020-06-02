from pymongo import MongoClient
import json

client = MongoClient(port=3154)

db = client["TwitterSearcher"]

collection = db["Old Tweets Data"]

cursor = collection.find({"coordinates": {"$ne" : None}})


previous_keys = set()

for entry in json.load(open("annotate.json")):
    previous_keys.add(entry["id"])
for entry in json.load(open("annotate_v2.json")):
    previous_keys.add(entry["id"])

annotation_entries = []
count = 600

for entry in cursor:

    id = str(entry["_id"])
    if id in previous_keys:
        continue
    if count == 0:
        break
    count -= 1

    text = entry["text"]
    annotated = False
    annotation = {}

    annotation["accident_related"] = False
    annotation["informative"] = False
    annotation["num_killed"] = 0
    annotation["num_injured"] = 0
    annotation["key_term_killed"] = ""
    annotation["key_term_injured"] = ""
    annotation["num_vehicles"] = ""
    annotation["key_term_num_vehicles"] = ""

    ann_entry = {}
    ann_entry["id"] = id
    ann_entry["text"] = text
    ann_entry["is_annotated"] = annotated
    ann_entry["annotation"] = annotation
    print("Added")
    annotation_entries.append(ann_entry)



json.dump(annotation_entries, open("annotate_v3.json", "w+"))











