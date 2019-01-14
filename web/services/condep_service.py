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
        sense_data = verb_details.database_ids[0] # type: SenseData
        hypernyms = sense_data.hypernyms

        try:
            synset = hypernyms[0] # type: str
        except IndexError:
            return None

        try:
            return condep_verbs.dictionary[synset]
        except KeyError:

            verbs_in_synset = directory_service.get_verbs_in_synset(synset) # type: List[str]
            for hyper_verb in verbs_in_synset:
                new_cd = get_condep_for_verb(hyper_verb)
                if new_cd:
                    return new_cd

            return None

if __name__ == "__main__":
    get_condep_for_verb('generate')