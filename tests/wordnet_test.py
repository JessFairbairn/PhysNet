import unittest

from nltk.corpus import wordnet as wn

import web.services.wordnet_service as wordnet_service
from web.services.verb_definition import SenseData

class WordNetRetrievalTests(unittest.TestCase):
    def test_dontCrashWhenNoWN(self):
        data = SenseData()
        
        wordnet_service.get_hypernyms(data)

    def test_GetsHypernymWhenSingle(self):
        self.skipTest()
        key = 'rotate%2:38:01'
        result = wn.lemma_from_key(key + '::').synset().hypernyms()
        pass
