import sys

from nltk.corpus import wordnet as wn

from web.services.verb_definition import VerbData

def get_hypernyms(verb:VerbData):
    if len(verb.wordnet) == 0:
        return []
    elif len(verb.wordnet) > 1:
        print('Multiple wordnet senses for verb: ', verb.wordnet) #TODO: handle this
        
    hypernyms = wn.lemma_from_key(verb.wordnet[0] + '::').synset().hypernyms()

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