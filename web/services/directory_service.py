import inspect
import json
import os
import typing

# from classes.verb_definition import VerbDefinition
from .verb_definition import VerbDefinition, SenseData

import condep.definitions.verbs as condep_verbs


def _decode_complex(dct: dict):

    possible_classes = [SenseData, VerbDefinition]

    for possible_class in possible_classes:

        is_member = _is_instance_of_class(dct, possible_class)
        if not is_member:
            continue

        obj = possible_class() # Assumes a constructor without arguments!
        for key, value in dct.items():
            setattr(obj, key, value)
        return obj
    
    # if it couldn't be decoded into one of those, just return the input dict
    return dct

def _is_instance_of_class(dct:dict, class_to_check:type):
    members = inspect.getmembers(
        class_to_check, lambda a: not(inspect.isroutine(a)))
    members = list(filter(lambda tup: not tup[0].startswith('_'), members))
    members = list(map(lambda tup: tup[0], members))
    is_member = set(dct.keys()).issubset(members)
    return is_member


def get_verb(verb: str):
    static = _get_static_folder()
    with open(f"{static}/results.json", "r") as tempFile:
        directory = json.load(tempFile, object_hook=_decode_complex)

        verb_def = directory.get(verb)

        try:
            condep = condep_verbs.dictionary[verb]
            verb_def.condep = condep

        except (KeyError, AttributeError):
            pass

        return verb_def

def get_verb_details():
    static = _get_static_folder()
    with open(f"{static}/results.json", "r") as tempFile:
        directory = json.load(tempFile, object_hook=_decode_complex)
        return directory

def get_verb_list():
    static = _get_static_folder()
    with open(f"{static}/results.json", "r") as tempFile:
        directory = json.load(tempFile)  # Type: dict[str]

        # turn into list of tuples
        tuples = directory.items()

        tuples = sorted(
            list(tuples), key=lambda verb: verb[1]['score'], reverse=True)

        verb_list = [verb[0] for verb in tuples]

        return verb_list


def _get_static_folder():
    #     return os.environ.get('STATIC_DIR', 'static')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    root = dir_path.split('/')
    try:
        index = root.index('PhysNet')
        if index > -1:
            return '/'.join(root[0:index + 1]) + '/web/static'
    except ValueError:

        pwd = os.path.dirname(os.path.realpath(__file__))
        root = pwd.split('/')
        if root[-1] == 'web':
            return 'static'
        else:
            return 'web/static'
