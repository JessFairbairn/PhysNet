from unittest import mock
from unittest.mock import patch
import unittest

from web.services import condep_service

import condep

class ConDepTests(unittest.TestCase):

    def test_returnsVerbWhenDefined(self):
        result = condep_service.get_condep_for_verb('emit')
        self.assertIsInstance(result, condep.parsing.cd_definitions.CDDefinition)

    def test_lookingUpByVerbInherets(self):
        fake_cd_dict = {'generate':condep.parsing.cd_definitions.CDDefinition()}

        with patch.dict('condep.definitions.verbs.dictionary', fake_cd_dict, clear=True):
            result = condep_service.get_condep_for_verb('generate')
            self.assertIsInstance(result, condep.parsing.cd_definitions.CDDefinition)
        
