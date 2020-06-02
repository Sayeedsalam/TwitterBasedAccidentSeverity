from pprint import pprint
import nltk
nltk.data.path.append("/Volumes/Untitled 2/Users/sayeed")

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
from allennlp.predictors.predictor import Predictor
predictor = Predictor.from_path("bert-base-srl-2019.06.17.tar.gz")

#matching two strings based on what they mean, not how they are written
from pymongo import MongoClient
import json

def identify_parts(part_name, tags, words):
    start_tag = "B-"+part_name
    cont_tag = "I-"+part_name

    parts_list = []
    temp = ""
    for i in range(len(tags)):
        if tags[i] == start_tag:
            if temp == "":
                temp = words[i]
            else:
                parts_list.append(temp)
                temp = words[i]
        elif tags[i] == cont_tag:
            temp = temp + " "+words[i]
        else:
             if temp != "":
                 parts_list.append(temp)
                 temp = ""

    return parts_list



client = MongoClient(port=3154)
print("Connected to DB")
db = client["TwitterSearcher"]

collection = db["Old Tweets Data"]

cursor = collection.find({"coordinates": {"$ne" : None}})


previous_keys = set()

# for entry in json.load(open("annotate.json")):
#     previous_keys.add(entry["id"])
#
annotation_entries = []
count = 300

for entry in cursor:

    # id = str(entry["_id"])
    # if id in previous_keys:
    #     continue
    # if count == 0:
    #     break
    # count -= 1

    text = entry["text"]
    result = predictor.predict(
        sentence=text.lower()
    )
    words = result["words"]
    processed_entry = {"text": text, "tweet_id": str(entry["_id"]), "location":{}}

    for entry in result["verbs"]:
        arr = identify_parts("V", entry["tags"], words)
        if len(arr) == 0:
            continue
        verb = identify_parts("V", entry["tags"], words)[0]
        verb = lemmatizer.lemmatize(verb, "v")

        arg1 = " ".join(identify_parts("ARG1", entry["tags"], words)).strip()
        arg0 = " ".join(identify_parts("ARG0", entry["tags"], words)).strip()
        arg_loc = " ".join(identify_parts("ARGM-LOC", entry["tags"], words)).strip()

        processed_entry["location"][verb] = arg_loc
    db.processed_entry.insert(processed_entry)
    print("Inserted ", id)






    print("Added")



# json.dump(annotation_entries, open("annotate_v2.json", "w+"))
#
#
#
# def string_match(str1, str2):
#     #need implementation
#     return str1.lower() == str2.lower()
#
# #do cluster analysis to extract more accident related verbs
# def cluster_search(tweets, incident_info, current_verb_list):
#     new_verbs = []
#
#     for tweet in tweets:
#         result = predictor.predict(
#           sentence=tweet.lower()
#         )
#
#         for entry in result["verbs"]:
#
#             verb = identify_parts("V", entry["tags"], words)[0]
#             verb = lemmatizer.lemmatize(verb, "v")
#             if verb in current_verb_list:
#                 continue
#             arg1 = " ".join(identify_parts("ARG1", entry["tags"], words)).strip()
#             arg0 = " ".join(identify_parts("ARG0", entry["tags"], words)).strip()
#             arg_loc = " ".join(identify_parts("ARGM-LOC", entry["tags"], words)).strip()
#             if string_match(incident_info, arg1):
#                  new_verbs.append((verb, "ARG1"))
#             elif string_match(incident_info, arg0):
#                  new_verbs.append((verb, "ARG0"))
#         return new_verbs
#
#
#
#
#
#
#
# tweets_file = open("cluster_test.txt", "r")
#
# incident_info = None
# for line in tweets_file:
#     result = predictor.predict(
#       sentence=line.lower()
#     )
#
#     #pprint(result)
#
#     #accident_verbs = ["injure", "die", "involve", "result", "cause", "kill"]
#     accident_verbs = ["kill"]
#
#     words = result["words"]
#     not_processed_tweets = []
#     print("Tweet : "+line)
#     verb_flag = False
#
#     for entry in result["verbs"]:
#
#         verb = identify_parts("V", entry["tags"], words)[0]
#         print(lemmatizer.lemmatize(verb, "v"))
#         if lemmatizer.lemmatize(verb, "v") in accident_verbs:
#             print(verb)
#             verb_flag = True
#             print("ARG1: "+ " ".join(identify_parts("ARG1", entry["tags"], words)).strip())
#             print("ARG0: "+ " ".join(identify_parts("ARG0", entry["tags"], words)).strip())
#             print("ARG-LOC: "+" ".join(identify_parts("ARGM-LOC", entry["tags"], words)).strip())
#             incident_info = " ".join(identify_parts("ARG1", entry["tags"], words)).strip()
#
#     if not verb_flag:
#
#         not_processed_tweets.append(line)
#         print("Appending")
#
#
# print(cluster_search(not_processed_tweets, incident_info, accident_verbs))
#




















