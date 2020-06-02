from gensim.similarities import docsim
from nltk.corpus import wordnet as wn
import nltk
from nltk.tokenize import word_tokenize
nltk.data.path.append("/Volumes/Untitled 2/Users/sayeed")
import gensim.downloader as api

word_vectors = api.load("glove-wiki-gigaword-100")

#calculates the similarity of two verbs
def verb_similarity(verb1, verb2):
    # #wordnet based
    # synset_verb1 = wn.synset(verb1+".v.01")
    # synset_verb2 = wn.synset(verb2+".v.01")
    #
    # return synset_verb1.path_similarity(synset_verb2)

    #word2vec based
    return word_vectors.n_similarity([verb1],[verb2])




#calculates similarity between arguments in the verb
def arg_similarity(phrase1 ,phrase2):

    words1 = word_tokenize(phrase1.lower())
    words2 = word_tokenize(phrase2.lower())
    return word_vectors.n_similarity(words1, words2)











print(verb_similarity("wound", "injure"))

print(verb_similarity("groomsman", "car"))


print(arg_similarity("man", "a person"))