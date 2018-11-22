from unittest import mock
from unittest.mock import patch
import unittest

from web.services import verbnet_service

class VerbNetIdRetrievalTests(unittest.TestCase):
    def test_GetsIdCorrectly_WhenMultipleInstances(self):
        self.skipTest('Multiple instances not yet working properly')
        data = verbnet_service.get_corpus_ids('ingest')

        self.assertEqual("absorb-39.8" , data.verbnet)

    def test_GetsIdCorrectly(self):
        data = verbnet_service.get_corpus_ids('capitulate')

        self.assertEqual("acquiesce-95.1"  , data.verbnet)

    def test_GetsIdFromSubgroupCorrectly(self):
        data = verbnet_service.get_corpus_ids('submit')

        self.assertEqual("acquiesce-95.1", data.verbnet)

class PropBankRetrievalTests(unittest.TestCase):
    def test_GetsCodeCorrectly(self):
        data = verbnet_service.get_corpus_ids('ingest')

        self.assertEqual('ingest.01', data.propbank)

    def test_GetsGroupingFromSubgroupCorrectly(self):
        data = verbnet_service.get_corpus_ids('consent')

        self.assertEqual('consent.01', data.propbank)

class WordNetRetrievalTests(unittest.TestCase):
    def test_GetsCodeCorrectly_WhenSingleWordNetCode(self):
        data = verbnet_service.get_corpus_ids('ingest')

        self.assertEqual("ingest%2:34:00" , data.wordnet[0])
        self.assertEqual(1 , len(data.wordnet))

    def test_GetsCodeCorrectly_WhenMultipleWordNetCodes(self):
        data = verbnet_service.get_corpus_ids('absorb')

        self.assertEqual(2 , len(data.wordnet))
        self.assertEqual("absorb%2:35:00" , data.wordnet[0])

    def test_GetsCodeFromSubgroupCorrectly(self):
        data = verbnet_service.get_corpus_ids('consent')

        self.assertEqual('consent%2:32:00', data.wordnet[0])

    def test_HandlesVerbsWithoutWN(self):
        data = verbnet_service.get_corpus_ids('activate')

        self.assertEqual(0, len(data.wordnet))

class VerbNetPhysicsDetection(unittest.TestCase):

    def test_FiltersWordsWhenAgentIsOrganisation(self):
        self.assertFalse(verbnet_service.is_physics_verb('extort'))

    def test_FiltersWordsWhenRecipientIsOrganisation(self):
        self.skipTest('Predict not valid example')
        self.assertFalse(verbnet_service.is_physics_verb('predict'))

    def test_FiltersWordsWithBenefitary(self):
        self.assertFalse(verbnet_service.is_physics_verb('award'))
