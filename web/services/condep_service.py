import typing
try:
    from web.services import directory_service
    from web.services.verb_definition import SenseData
except ImportError:
    from services import directory_service
    from services.verb_definition import SenseData

import condep.definitions.verbs as condep_verbs

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

            try:
                return condep_verbs.dictionary[synset]
            except KeyError:

                verbs_in_synset = directory_service.get_verbs_in_synset(synset) # type: List[str]
                for hyper_verb in verbs_in_synset:
                    if hyper_verb == verb:
                        print('Recursive error for verb ' + verb)
                        continue
                        
                    new_cd = get_condep_for_verb(hyper_verb)
                    if new_cd:
                        return new_cd

                continue
        return None

if __name__ == "__main__":
    get_condep_for_verb('generate')