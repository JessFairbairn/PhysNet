import os
import sys

import xml.etree.ElementTree as ET


dir_path = os.path.dirname(os.path.realpath(__file__))
root = dir_path.split('/')
index = root.index('PhysNet')
sys.path.append('/'.join(root[0:index + 1]) + '/ConDep')

import ConDep.condep as condep
import web.services.directory_service as directory_service
from web.services.verb_definition import SenseData

from web.services import wordnet_service


def is_physics_verb(verb:str):
    files_in_dir = os.listdir('verbnet')
    found_in_verbnet = False

    for verb_file in files_in_dir:
        if not verb_file.endswith('.xml'):
            continue
        tree = ET.parse('verbnet/' + verb_file)
        root = tree.getroot()

        found_verb = root.find(f'MEMBERS/MEMBER[@name="{verb}"]')
        

        if found_verb is None:
            found_subclass = root.find(f'SUBCLASSES/VNSUBCLASS/MEMBERS/MEMBER[@name="{verb}"]')
            if found_subclass is None:
                continue
            else:
                found_in_verbnet = True
        else:
            found_in_verbnet = True

        if _root_is_physics_sense(root):
            return True

    if not found_in_verbnet:
        print(f'Verb "{verb}" not in VerbNet')
        return True
    else:
        return False


def get_corpus_ids(verb:str):
    senses = []

    files_in_dir = os.listdir('verbnet')

    for verb_file in files_in_dir:
        if not verb_file.endswith('.xml'):
            continue
        tree = ET.parse('verbnet/' + verb_file)
        root = tree.getroot()

        found_verb = root.find(f'MEMBERS/MEMBER[@name="{verb}"]')

        if not _root_is_physics_sense(root):
            continue
        
        data = SenseData()
        if found_verb is not None:
            data.verbnet = root.attrib['ID']
            data.propbank = found_verb.attrib['grouping']
            wordnet_codes = found_verb.attrib['wn']
            if wordnet_codes == '':
                data.wordnet = []
            else:
                data.wordnet = wordnet_codes.split(' ')
            data.hypernyms = wordnet_service.get_hypernyms(data)
            senses.append(data)
        else:        
            found_subclass = root.find(f'SUBCLASSES/VNSUBCLASS/MEMBERS/MEMBER[@name="{verb}"]')
            if found_subclass is not None:
                data.verbnet = root.attrib['ID']
                data.propbank =  found_subclass.attrib['grouping']
                wordnet_codes = found_subclass.attrib['wn']
                if wordnet_codes == '':
                    data.wordnet = []
                else:
                    data.wordnet = wordnet_codes.split(' ')
                data.hypernyms = wordnet_service.get_hypernyms(data)
                senses.append(data)

    return senses


def _root_is_physics_sense(root:ET.Element):
    if root.find('THEMROLES/THEMROLE[@type="Beneficiary"]'):
        return False

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