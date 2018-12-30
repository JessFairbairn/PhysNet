import unittest

from nltk.corpus import wordnet as wn

import web.services.wordnet_service as wordnet_service
from web.services.verb_definition import SenseData

class WordNetVerbTests(unittest.TestCase):
    def test_wontfinditonverbnet(self):
        self.assertFalse(wordnet_service.is_verb('car'))

    def test_onwordnet(self):
        self.assertTrue(wordnet_service.is_verb('dog'))

    def test_gets_keys(self):
        senses = wordnet_service.get_corpus_ids('dog')
        for sense in senses:
            self.assertEqual(len(sense.wordnet), 1)
            self.assertTrue(sense.wordnet[0])
            self.assertTrue(sense.hypernyms)


class WordNetRetrievalTests(unittest.TestCase):
    def test_dontCrashWhenNoWN(self):
        data = SenseData()
        
        wordnet_service.get_hypernyms(data)

    def test_GetsHypernymWhenSingle(self):
        self.skipTest('dunno')
        key = 'rotate%2:38:01'
        result = wn.lemma_from_key(key + '::').synset().hypernyms()
        pass
