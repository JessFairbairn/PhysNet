import json

def get_verb(verb:str):
    with open("web/static/results.json", "r") as tempFile:
        directory = json.load(tempFile)
        
        return directory.get(verb)
        
def get_verb_list():
    with open("web/static/results.json", "r") as tempFile:
        directory = json.load(tempFile)
        
        return [verb for verb in directory]