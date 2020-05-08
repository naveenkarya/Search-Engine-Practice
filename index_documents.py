import re
from nltk.stem.snowball import SnowballStemmer
from word_service import WordsService
from pymongo import MongoClient
import math
from config import get_config

'''
Reads data from a file
'''
def read_file(file_name):
    with open(file_name) as file:
        data = file.read()
        return data

'''
Gets all the indexes from DB, computes tf-idf, 
sort the documents based on tf-idf,
and update the documents in the DB
'''
def tf_idf ():
    wordService = WordsService()
    wc = wordService.find_all()
    totalTerms = wordService.get_total_terms()
    for pair in wc.items():
        idf = math.log(len(totalTerms)/len(pair[1]), 10)
        for doc in pair[1].items():
            tf = doc[1]["count"]/totalTerms[doc[0]]
            doc[1]["tfidf"] = tf*idf
        sortedList = sorted(pair[1].items(), key = lambda t : t[1]["tfidf"], reverse=True)
        sortedDocs = {}
        for details in sortedList:
            sortedDocs[details[0]] = details[1]
        wordService.update_word(pair[0], sortedDocs)
    return wc

'''
Helper method to get the matching text from the document
'''
def getMatchingText(document, index, count):
    startIndex = 0
    if index - count > 0:
        startIndex = index - count
    return document[startIndex:index+count]

'''
Indexes the documents in DB in the form of inverted index
'''
def indexDocuments(documentNames):
    docPath = get_config("Config", "DOCUMENT_PATH")
    eng_stemmer = SnowballStemmer("english")
    stop_words = read_file('stop_words.txt').split(',')
    wc = {}
    totalTerms = {}
    for documentName in documentNames:
        document = read_file(docPath + documentName).lower()
        words = re.findall('\w{2,}', document)
        total = 0
        for wordUnstemmed in words:
            if wordUnstemmed not in stop_words:
                word = eng_stemmer.stem(wordUnstemmed)
                total = total + 1
                docs = wc.get(word, {})
                wc[word] = docs
                count = wc[word].get(documentName, {"count":0, "matchingText":""}).get("count") + 1
                index = document.find(" "+wordUnstemmed)
                matchingText = getMatchingText(document, index, 20)
                if count == 1:
                    wc[word][documentName] = {"count" : count, "matchingText": matchingText}
                else:
                    wc[word][documentName]["count"] = count
        totalTerms[documentName] = total

    wordService = WordsService()
    wordService.update_total_terms(totalTerms)
    wordService.insert_words(wc)


'''
First index documents and then perform tf-idf. Just an example.
'''
indexDocuments(['doc1', 'doc2','doc3', 'doc4','doc5', 'doc6'])
tf_idf()
