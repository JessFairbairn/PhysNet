import unittest

from process import Processor

class TagWordsWithPOS(unittest.TestCase):
    def test_tagsCorrectly(self):
        self.skipTest('slow- integration test')
        
        blah = Processor()
        sentence = "Because such compact stars have high gravitational fields, the material falls with a high velocity towards the compact star, usually colliding with other accreted material en route, forming an accretion disk."

        sentence2 = "Since it is difficult to define where the photosphere of a star ends and the chromosphere begins, astrophysicists usually rely on the Eddington Approximation to derive the formal definition of lol."

        list_of_verbs = blah._list_verbs(sentence2)

        self.assertNotIn('astrophysicists', list_of_verbs)

        