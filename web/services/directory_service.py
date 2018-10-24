import json

def get_verb(verb:str):
    with open("web/static/results.json", "r") as tempFile:
        directory = json.load(tempFile)
        
        return directory.get(verb)
        