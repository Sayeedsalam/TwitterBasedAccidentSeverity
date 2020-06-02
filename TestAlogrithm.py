import json
from pprint import pprint
import nltk
nltk.data.path.append("/Volumes/Untitled 2/Users/sayeed")

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import gensim.downloader as api

word_vectors = api.load("glove-wiki-gigaword-100")

lemmatizer = WordNetLemmatizer()
from allennlp.predictors.predictor import Predictor
predictor = Predictor.from_path("/Volumes/Untitled 2/Users/sayeed/bert-base-srl-2019.06.17.tar.gz")

#matching two strings based on what they mean, not how they are written



def calc_similarity(phrase1 ,phrase2):
    try:
        words1 = word_tokenize(phrase1.lower())
        words2 = word_tokenize(phrase2.lower())
        return word_vectors.n_similarity(words1, words2)
    except KeyError:
        return 0.0







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
    if temp != "":
        parts_list.append(temp)

    return parts_list


tweets_file = open("cluster_test.txt", "r")

incident_info = None

accident_verbs = ["injure", "die", "involve", "result", "cause", "kill"]

def accident_related_args(text):


    result = predictor.predict(
      sentence=text.lower()
    )


    #accident_verbs = ["kill"]

    words = result["words"]
    not_processed_tweets = []
    print("Tweet : "+text)
    verb_flag = False
    info = {}

    for entry in result["verbs"]:
        print(result["verbs"])
        verb = identify_parts("V", entry["tags"], words)[0]
        verb = lemmatizer.lemmatize(verb, "v")
        if verb in accident_verbs:
            print(verb)
            verb_flag = True
            arg1 = " ".join(identify_parts("ARG1", entry["tags"], words)).strip()
            arg2 =  " ".join(identify_parts("ARG0", entry["tags"], words)).strip()
            arg_loc = " ".join(identify_parts("ARGM-LOC", entry["tags"], words)).strip()

            info[verb] = {"ARG1": arg1, "ARG2": arg2, "ARG_LOC": arg_loc}

    return info


annotated_tweets = json.load(open("annotations.json", "r"))
count_annotated_tweet=0

count_identified=0

for annotated_tweet in annotated_tweets:
    print(annotated_tweet.keys())
    if annotated_tweet["is_annotated"] and "informative" in annotated_tweet["annotation"]:
        if annotated_tweet["annotation"]["informative"] == False:
            continue
        count_annotated_tweet += 1

        info = accident_related_args(annotated_tweet["text"])


        annotated_killed = annotated_tweet["annotation"]["key_term_killed"]
        #annotated_injured = annotated_tweet["key_term_killed"]
        if annotated_killed == "":
            count_annotated_tweet -= 1


            continue
        highest_match = 0.0

        match_verb = ""
        for verb in info:
            sim_val = calc_similarity(info[verb]["ARG1"]+" "+verb, annotated_killed)
            print(info[verb]["ARG1"], annotated_killed, sim_val, "\n")
            if sim_val > highest_match:
                match_verb = verb
                highest_match = sim_val


        if highest_match > 0.8:
            print("Significant Match with VERB: ", verb)
            count_identified += 1


print(count_annotated_tweet, count_identified)



























