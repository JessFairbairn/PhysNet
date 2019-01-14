import json
import tempfile
import unittest

import process
from web.services.verb_definition import SenseData
from web.services import directory_service

class process_tests(unittest.TestCase):

    def test_jsonEncodesVerbDefinition(self):
        test_list = set([1,2,3])
        definition = SenseData()
        definition.hypernyms = test_list

        result = process._encode_for_json(definition)

        self.assertIsInstance(result['hypernyms'], list)

    def test_integration(self):
        tempFileWrapepr = tempfile.NamedTemporaryFile(suffix='.json')

        test_list = set([1,2,3])
        definition = dict()
        definition['random_key'] = test_list

        new_dict = {'run':SenseData()}

        synsets_list = {
            'blah.l.01':test_list
        }

        file_data = {
            'directory': new_dict,
            'synsets': synsets_list
        }

        with open(tempFileWrapepr.name, "w") as tempFile:
            json.dump(file_data, tempFile, default=process._encode_for_json)

        with open(tempFileWrapepr.name, "r") as tempFile:
            loaded = json.load(tempFile, object_hook=directory_service._decode_complex)
            self.assertEqual(len(loaded['synsets']['blah.l.01']), 3)