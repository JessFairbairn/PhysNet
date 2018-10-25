import json
import os
import typing

def get_verb(verb:str):
    static = _get_static_folder()
    with open(f"{static}/results.json", "r") as tempFile:
        directory = json.load(tempFile)
        
        return directory.get(verb)
        
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