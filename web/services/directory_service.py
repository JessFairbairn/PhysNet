import inspect
import json
import os
import typing

try:
    # from classes.verb_definition import VerbDefinition
    from .verb_definition import VerbDefinition, SenseData

    import condep.definitions.verbs as condep_verbs
except ImportError:
    raise


def get_verb(verb: str):
        directory = _get_file_data()['directory']

        verb_def = directory.get(verb) # type: VerbDefinition

        # try:
        #     condep = condep_verbs.dictionary[verb]
        #     verb_def.condep = condep

        # except (KeyError, AttributeError):
        #     pass

        return verb_def

def get_verb_details():
    return _get_file_data()['directory']

def get_verb_list():
    
    directory = _get_file_data()['directory']  # Type: dict[str]

    # turn into list of tuples
    tuples = directory.items()

    tuples = sorted(
        list(tuples), key=lambda verb: verb[1].score, reverse=True)

    verb_list = [verb[0] for verb in tuples]

    return verb_list

def calculate_verbs_in_synsets(synset:str):
    directory = get_verb_details() # type: List[VerbDefinition]

    verbs_in_synset = []
    for k, verb_data in directory.items():
        if list(filter(lambda sense: sense.synset == synset, verb_data.database_ids)):
            verbs_in_synset.append(k)
    return verbs_in_synset

def get_verbs_in_synset(synset:str):
    try:
        return _get_file_data()['synsets'][synset]
    except KeyError:
        return []

# PRIVATE #

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

def _get_file_data():
    static = _get_static_folder()
    with open(f"{static}/results.json", "r") as tempFile:
        file_data = json.load(tempFile, object_hook=_decode_complex)
        return file_data