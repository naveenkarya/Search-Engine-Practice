from pymongo import MongoClient
from random import randint
from config import get_config
# use indexDB
# db.words.find()

class WordsService:
    def __init__(self):
        client = MongoClient(get_config("DB", "CONNECTION_URL"))
        db = client.indexDB
        self.words = db.words
        self.totalTerms = db.totalTerms

    '''
    Searches for a word and returns list of documents
    '''
    def get(self, word):
        wordFound = self.words.find_one({'word': word})
        if wordFound is None:
            return None
        else:
            return wordFound.get('documents', None)

    '''
    Inserts/Merges words in DB
    '''
    def insert_words(self, wordMap):
        newWordList = []
        for word in wordMap:
            docsFromDB = self.get(word)
            if docsFromDB is None:
                newWordList.append({
                    "word" : word,
                    "documents" : wordMap.get(word)
                })
            else:
                for fileName in wordMap.get(word):
                    docsFromDB[fileName] = wordMap.get(word).get(fileName)                        
                self.words.update_one({'word': word}, {"$set" : {"documents" : docsFromDB}})
        if(len(newWordList) > 0):
            self.words.insert(newWordList)
    
    '''
    Update the index of a word in DB
    '''
    def update_word(self, word, documents):
        self.words.update_one({'word': word}, {"$set" : {"documents" : documents}})
    
    def update_total_terms(self, totalTerms):
        for pair in totalTerms.items():
            self.totalTerms.update_one({"fileName" : pair[0]}, {"$set" : {"totalWords" : pair[1]}}, True)        
    
    def get_total_terms(self):
        terms = {}
        for term in self.totalTerms.find():
            terms[term["fileName"]] = term["totalWords"]
        return terms
    
    def find_all(self):
        total = {}
        for doc in self.words.find():
            total[doc['word']] = doc['documents']
        return total

    


