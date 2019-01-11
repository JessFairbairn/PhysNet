from unittest import mock
from unittest.mock import patch
import unittest

from web.services import directory_service

class SynsetTests(unittest.TestCase):
    def test_returnsEmptyList_whenNoVerbsInSet(self):
        results = directory_service.get_verbs_in_synset('blahdeblah')
        self.assertFalse(results)

    def test_returnsListWithItems_whenVerbsInSet(self):
        results = directory_service.get_verbs_in_synset('magnetize.v.01')
        self.assertTrue(results)
        self.assertTrue(all(map(lambda name: type(name) == str, results)))