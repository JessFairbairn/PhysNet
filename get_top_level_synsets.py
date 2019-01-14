import typing

from web.services import directory_service

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

        

for lemma, verb_data in directory.items():
    for sense in verb_data.database_ids:

        if not sense.synset:
            continue

        for hypernym in sense.hypernyms:
            # if hypernym not in list_of_synsets:
            #     continue
            
            synsets_with_hypernyms.add(sense.synset)
            
            if hypernym in children.keys():
                children[hypernym].add(sense.synset)
            else:
                children[hypernym] = set([sense.synset])

synsets_with_hyponyms = set(children.keys())
top_level_synsets = list_of_synsets.difference(synsets_with_hypernyms)

with open('top_level_synsets.txt','w') as syn_file:
    
    syn_file.write('\n'.join(top_level_synsets))