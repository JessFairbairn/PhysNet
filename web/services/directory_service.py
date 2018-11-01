import inspect
import json
import os
import typing

# from classes.verb_definition import VerbDefinition
from web.services.verb_definition import VerbDefinition

import condep.definitions.verbs as condep_verbs

def _decode_complex(dct:dict):

        members = inspect.getmembers(VerbDefinition, lambda a:not(inspect.isroutine(a)))
        members = list(filter(lambda tup: not tup[0].startswith('_'), members))
        members = list(map(lambda tup: tup[0], members))
        if not set(dct.keys()).issubset(members):
                return dct

        obj = VerbDefinition()
        for key, value in dct.items():
                setattr(obj, key, value)
        return obj

def get_verb(verb:str):
    static = _get_static_folder()
    with open(f"{static}/results.json", "r") as tempFile:
        directory = json.load(tempFile, object_hook=_decode_complex)
        
        verb_def = directory.get(verb)
        

        try:
                condep = condep_verbs.dictionary[verb]
                verb_def.condep = condep
                
        except KeyError:
                pass

        return verb_def
        
def get_verb_list():
    static = _get_static_folder()
    with open(f"{static}/results.json", "r") as tempFile:
        directory = json.load(tempFile) #Type: dict[str]

        # turn into list of tuples
        tuples = directory.items()

        tuples = sorted(list(tuples), key=lambda verb: verb[1]['score'], reverse=True)

        verb_list = [verb[0] for verb in tuples]
        
        return verb_list

def _get_static_folder():
    return os.environ.get('STATIC_DIR', 'static')

