from unittest import mock
from unittest.mock import patch
import unittest

from web.services import verbnet_service

class VerbNetIdRetrievalTests(unittest.TestCase):
    def test_GetsIdCorrectly_WhenMultipleInstances(self):
        self.skipTest('Multiple instances not yet working properly')
        data = verbnet_service.get_corpus_ids('ingest')

        self.assertEqual("absorb-39.8" , data[0].verbnet)

    def test_GetsIdCorrectly(self):
        data = verbnet_service.get_corpus_ids('expire')

        self.assertEqual("break_down-45.8"  , data[0].verbnet)

    def test_GetsIdFromSubgroupCorrectly(self):
        data = verbnet_service.get_corpus_ids('swallow')

        self.assertEqual("gobble-39.3-2", data[0].verbnet)

# class PropBankRetrievalTests(unittest.TestCase):
#     def test_GetsCodeCorrectly(self):
#         data = verbnet_service.get_corpus_ids('ingest')

#         self.assertEqual('ingest.01', data[0].propbank)

#     def test_GetsGroupingFromSubgroupCorrectly(self):
#         data = verbnet_service.get_corpus_ids('consent')

#         self.assertEqual('consent.01', data[0].propbank)

class WordNetRetrievalTests(unittest.TestCase):
    def test_GetsCodeCorrectly_WhenSingleWordNetCode(self):
        data = verbnet_service.get_corpus_ids('ingest')

        self.assertEqual("ingest%2:34:00" , data[0].wordnet[0])
        self.assertEqual(1 , len(data[0].wordnet))

    def test_GetsCodeCorrectly_WhenMultipleWordNetCodes(self):
        self.skipTest('Not working, needs review')
        data = verbnet_service.get_corpus_ids('absorb')

        self.assertEqual(2 , len(data[0].wordnet))
        self.assertEqual("absorb%2:35:00" , data[0].wordnet[0])

    def test_GetsCodeFromSubgroupCorrectly(self):
        self.skipTest('doesn\'t work because consent not not a physics verb')
        data = verbnet_service.get_corpus_ids('consent')

        self.assertEqual('consent%2:32:00', data[0].wordnet[0])

    def test_HandlesVerbsWithoutWN(self):
        data = verbnet_service.get_corpus_ids('activate')

        self.assertEqual(0, len(data[0].wordnet))

class VerbNetPhysicsDetection(unittest.TestCase):

    def test_FiltersWordsWhenAgentIsOrganisation(self):
        self.assertFalse(verbnet_service.is_physics_verb('extort'))

    def test_FiltersWordsWhenRecipientIsOrganisation(self):
        self.skipTest('Predict not valid example')
        self.assertFalse(verbnet_service.is_physics_verb('predict'))

    def test_FiltersWordsWithBenefitary(self):
        self.assertFalse(verbnet_service.is_physics_verb('award'))

    def test_FiltersWordsWithExperiencer(self):
        self.assertFalse(verbnet_service.is_physics_verb('recognise'))

class VerbNeterrorRaising(unittest.TestCase):

    def test_RaisesErrorWhenNotFound(self):
        with self.assertRaises(verbnet_service.NotInVerbNetException) as context:
            
            verbnet_service.is_physics_verb('gjggfdfgdgf')

    def test_DoesntRaiseErrorWhenNotPhysicsVerb(self):
            
        verbnet_service.is_physics_verb('measure')

class VerbNetPhysicsClassDetection(unittest.TestCase):
    def test_(self):
        themroles = [
            {'type': 'Agent', 'modifiers': 
                [{'value': '+', 'type': 'animate'}, {'value': '+', 'type': 'organization'}]},
            {'type': 'Theme', 'modifiers': []},
            {'type': 'Source', 'modifiers': []},
            {'type': 'Beneficiary', 'modifiers':
                [{'value': '+', 'type': 'animate'}]}
            ]

        self.assertFalse(
            verbnet_service._is_physics_class(themroles)
        )

#exmaple themroles:
# [{'type': 'Agent', 'modifiers': [{'value': '+', 'type': 'animate'}, {'value': '+', 'type': 'organization'}]}, {'type': 'Theme', 'modifiers': []}, {'type': 'Source', 'modifiers': []}, {'type': 'Beneficiary', 'modifiers': [{'value': '+', 'type': 'animate'}]}]