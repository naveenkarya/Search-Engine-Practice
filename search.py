import math
from word_service import WordsService
from config import get_config
'''
search for a word in the indexes
'''
def search (word):
    limit = int(get_config("Config", "MAX_RESULTS"))
    wordService = WordsService()
    docs = wordService.get(word)
    if docs is None:
        return []
    else:
        list = []
        for doc in docs.items():
            list.append({"file" : doc[0], "matchingText":doc[1]["matchingText"], "count" : doc[1]["count"]})
        return {'result' : list[:limit]}

