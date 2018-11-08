import os
import sys

import xml.etree.ElementTree as ET


dir_path = os.path.dirname(os.path.realpath(__file__))
root = dir_path.split('/')
index = root.index('PhysNet')
sys.path.append('/'.join(root[0:index + 1]) + '/ConDep')

import ConDep.condep as condep
import web.services.directory_service as directory_service
from classes.verbs import VerbData


def is_physics_verb(verb:str):
    files_in_dir = os.listdir('verbnet')

    for verb_file in files_in_dir:
        if not verb_file.endswith('.xml'):
            continue
        tree = ET.parse('verbnet/' + verb_file)
        root = tree.getroot()

        found_verb = root.find(f'VNCLASS/MEMBERS/MEMBER[@name="{verb}"]')
        

        if found_verb is None:
            found_subclass = root.find(f'SUBCLASSES/VNSUBCLASS/MEMBERS/MEMBER[@name="{verb}"]')
            if found_subclass is None:
                continue

        return _check_root_selrests

    print(f'Verb "{verb}" not in VerbNet')
    return True


def get_corpus_ids(verb:str):
    data = VerbData()

    files_in_dir = os.listdir('verbnet')

    for verb_file in files_in_dir:
        if not verb_file.endswith('.xml'):
            continue
        tree = ET.parse('verbnet/' + verb_file)
        root = tree.getroot()

        found_verb = root.find(f'MEMBERS/MEMBER[@name="{verb}"]')

        #TODO: check selrests

        if found_verb is not None:
            data.verbnet = root.attrib['ID']
            data.propbank = found_verb.attrib['grouping']
            wordnet_codes = found_verb.attrib['wn']
            data.wordnet = wordnet_codes.split(' ')
        else:        
            found_subclass = root.find(f'SUBCLASSES/VNSUBCLASS/MEMBERS/MEMBER[@name="{verb}"]')
            if found_subclass is not None:
                data.verbnet = root.attrib['ID']
                data.propbank =  found_subclass.attrib['grouping']
                wordnet_codes = found_subclass.attrib['wn']
                data.wordnet = wordnet_codes.split(' ')

    return data


def _check_root_selrests(root:ET.Element):
    sel_rests = list(map(lambda ele: ele.attrib['type'],
            root.findall('THEMROLES/THEMROLE[@type="Agent"]/SELRESTRS/SELRESTR'))
        )
    if 'organization' in sel_rests:
        return False
    else:
        return True

if __name__ == '__main__':
    # verb_list = directory_service.get_verb_list()
    # removed_verbs = []
    # for verb in verb_list:
    #     if not is_physics_verb(verb):
    #         removed_verbs.append(verb)
    # pass
    is_physics_verb('list')