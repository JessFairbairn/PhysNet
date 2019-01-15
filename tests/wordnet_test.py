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


class WordnetSynsetRetrievalTests(unittest.TestCase):
    def test_getsSynsetFromKey(self):
        result = wordnet_service.get_synset_from_key('choke%2:35:00')
        
        self.assertEqual(result, 'choke.v.02')

class WordNetHypernymRetrievalTests(unittest.TestCase):
    def test_dontCrashWhenNoWN(self):
        data = SenseData()
        
        wordnet_service.get_hypernyms(data)

    def test_Shrug(self):
        self.skipTest('dunno')
        key = 'rotate%2:38:01'
        result = wn.lemma_from_key(key + '::').synset().hypernyms()
        pass

    def test_GetsHypernymWhenSingle(self):
        key = 'rotate%2:38:01'
        data = SenseData()
        data.wordnet = [key]

        result = wordnet_service.get_hypernyms(data)
        self.assertTrue(type(result) == list, 'should return a list')

        synset_name = result[0]
        split = synset_name.split('.')

        self.assertEqual(len(split), 3, 'should return a 3 part synset name')
        self.assertEqual(split[1], 'v', 'Should return a verb lol')
