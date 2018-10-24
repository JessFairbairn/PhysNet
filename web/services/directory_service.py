import json

def get_verb(verb:str):
    with open("../results.json", "r") as tempFile:
        directory = json.load(tempFile)
        
        return directory.get(verb)
        