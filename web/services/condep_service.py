import typing
try:
    from web.services import directory_service
    from web.services.verb_definition import SenseData
except ImportError:
    from services import directory_service
    from services.verb_definition import SenseData

import condep.definitions.verbs as condep_verbs
import condep.definitions.synsets as condep_synsets

# look up generate so it can inherit 'create'

def get_condep_for_verb(verb:str):
    try:
        return condep_verbs.dictionary[verb]
    except KeyError:
        verb_details = directory_service.get_verb(verb)
        for sense_data in verb_details.database_ids: # type: SenseData
            hypernyms = sense_data.hypernyms

            try:
                synset = hypernyms[0] # type: str
            except IndexError:
                continue

            synset_cd = get_condep_for_synset(synset, verb)
            if synset_cd:
                return synset_cd
            else:
                continue
        return None

def get_condep_for_synset(synset:str, verb:str=None):
    try:
        return condep_synsets.dictionary[synset]
    except KeyError:

        verbs_in_synset = directory_service.get_verbs_in_synset(synset) # type: List[str]
        for hyper_verb in verbs_in_synset:
            if verb and hyper_verb == verb:
                print('Recursive error for verb ' + verb)
                continue
                
            new_cd = get_condep_for_verb(hyper_verb)
            if new_cd:
                return new_cd
    return None

if __name__ == "__main__":
    get_condep_for_verb('generate')