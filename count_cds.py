import typing

from web.services import directory_service
from web.services import condep_service

directory = directory_service.get_verb_details() # Type: Dict

children = dict()
parent_lookup = dict()

list_of_synsets = set()
synsets_with_hypernyms = set()

for lemma, verb_data in directory.items():
    for sense in verb_data.database_ids:

        if not sense.synset:
            continue

        list_of_synsets.add(sense.synset)

num_with_cds = 0

for lemma, verb_data in directory.items():
    cd = condep_service.get_condep_for_verb(lemma)
    if cd:
        num_with_cds += 1

fraction = num_with_cds/len(directory.keys())
print('Number of verbs with CD definitions:', num_with_cds)
print(str(fraction*100) + '%')