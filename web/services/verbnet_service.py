import os
import sys

import xml.etree.ElementTree as ET


dir_path = os.path.dirname(os.path.realpath(__file__))
root = dir_path.split('/')
index = root.index('PhysNet')
sys.path.append('/'.join(root[0:index + 1]) + '/ConDep')

import ConDep.condep as condep
import web.services.directory_service as directory_service


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

        sel_rests = list(map(lambda ele: ele.attrib['type'],
            root.findall('THEMROLES/THEMROLE[@type="Agent"]/SELRESTRS/SELRESTR'))
        )
        if 'organization' in sel_rests:
            return False
        else:
            return True

    print(f'Verb "{verb}" not in VerbNet')
    return True

if __name__ == '__main__':
    # verb_list = directory_service.get_verb_list()
    # removed_verbs = []
    # for verb in verb_list:
    #     if not is_physics_verb(verb):
    #         removed_verbs.append(verb)
    # pass
    is_physics_verb('list')