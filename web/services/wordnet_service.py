import sys

from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError

from web.services.verb_definition import SenseData

def get_hypernyms(verb:SenseData):
    if len(verb.wordnet) == 0:
        return []
    elif len(verb.wordnet) > 1:
        print('Multiple wordnet senses for verb: ', verb.wordnet) #TODO: handle this
    try:
        hypernyms = wn.lemma_from_key(verb.wordnet[0] + '::').synset().hypernyms()
    except WordNetError as e:
        print("Error getting hypernyms for ", verb.wordnet[0], ': ', e)
        return []


    if len(hypernyms) > 1:
        print('Multiple hypernyms for verb! ', hypernyms)
    
    try:
        return hypernyms[0].lemma_names()
    except IndexError:
        return []

if '__main__' == __name__:
    verb = 'bisect'
    synsets = wn.synsets(verb, pos=wn.VERB)

    if len(synsets) > 1:
        raise NotImplementedError('Multiple synsets for verb ', verb)

    synset = synsets[0]

    hypernyms = synset.hypernyms()
    if len(hypernyms) > 1:
        print('multiple hypernyms', file = sys.stderr)

    pass