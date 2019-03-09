import json
import typing

from web.services import directory_service
from web.services import condep_service

directory = directory_service.get_verb_details() # Type: Dict

children_of_synsets = dict()
parent_lookup = dict()

direct_synsets = set()
synsets_with_hypernyms = set()

def _encode_for_json(obj):
    if type(obj) == set:
        return list(obj)
        
    output = obj.__dict__
    for key, value in output.items():
        if type(value) == set:
            output[key] = list(value)
    return output

for lemma, verb_data in directory.items():
    for sense in verb_data.database_ids:

        if not sense.synset:
            continue

        direct_synsets.add(sense.synset)

        

for lemma, verb_data in directory.items():
    for sense in verb_data.database_ids:

        if not sense.synset:
            continue

        for hypernym in sense.hypernyms:
            # if hypernym not in list_of_synsets:
            #     continue
            
            synsets_with_hypernyms.add(sense.synset)
            
            if hypernym in children_of_synsets.keys():
                children_of_synsets[hypernym].add(sense.synset)
            else:
                children_of_synsets[hypernym] = set([sense.synset])

synsets_with_hyponyms = set(children_of_synsets.keys())
all_synsets = direct_synsets.union(synsets_with_hyponyms)
top_level_synsets = all_synsets.difference(synsets_with_hypernyms)

synsets_needing_cd = []
for synset in top_level_synsets:
    
    cd = condep_service.get_condep_for_synset(synset)

    if cd:
        continue

    verbs = directory_service.get_verbs_in_synset(synset)
    if not verbs:
        synsets_needing_cd.append(synset)
        continue
        
    for verb in verbs:
        cd = condep_service.get_condep_for_verb(verb)
        if cd:
            break
    
    if not cd:
        synsets_needing_cd.append(synset)

with open('web/static/children_of_synsets.json','w') as hypo_file:
    
    json.dump(children_of_synsets, hypo_file, default=_encode_for_json)



with open('top_level_synsets.txt','w') as syn_file:
    
    syn_file.write('\n'.join(synsets_needing_cd))

