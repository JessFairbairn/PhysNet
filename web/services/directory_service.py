import json
import os

def get_verb(verb:str):
    static = _get_static_folder()
    with open(f"{static}/results.json", "r") as tempFile:
        directory = json.load(tempFile)
        
        return directory.get(verb)
        
def get_verb_list():
    static = _get_static_folder()
    with open(f"{static}/results.json", "r") as tempFile:
        directory = json.load(tempFile)
        
        return [verb for verb in directory]

def _get_static_folder():
                return os.environ.get('STATIC_DIR', 'static')