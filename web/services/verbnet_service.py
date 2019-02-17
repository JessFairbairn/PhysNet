import os
import sys

import nltk

dir_path = os.path.dirname(os.path.realpath(__file__))
root = dir_path.split('/')
index = root.index('PhysNet')
sys.path.append('/'.join(root[0:index + 1]) + '/ConDep')

import condep as condep
import web.services.directory_service as directory_service
from web.services.verb_definition import SenseData

from web.services import wordnet_service

vb = nltk.corpus.util.LazyCorpusLoader('verbnet3', nltk.corpus.reader.verbnet.VerbnetCorpusReader,r'(?!\.).*\.xml')



def is_physics_verb(verb:str):

    classids = vb.classids(lemma=verb)
    if not classids:
        raise NotInVerbNetException(f'Verb "{verb}" not in VerbNet')

    for classid in classids:
        themroles = _get_themroles_for_class_id(classid)

        if _is_physics_class(themroles):
            return True

    return False


def get_corpus_ids(verb:str):
    senses = []

    classids = vb.classids(lemma=verb)
    if not classids:
        raise NotInVerbNetException(f'Verb "{verb}" not in VerbNet')

    for class_id in classids:
        themroles = _get_themroles_for_class_id(class_id)

        if not _is_physics_class(themroles): # is this right?
            continue

        
        data = SenseData()
        
        data.verbnet = class_id
        # data.propbank = found_verb.attrib['grouping']

        # Get wordnet codes
        xml = vb.vnclass(class_id)
        member_node = xml.find(f'*/MEMBER[@name="{verb}"]') # TODO: Assuming only one node- check?
        wordnet_codes = member_node.attrib['wn']

        if wordnet_codes == '':
            data.wordnet = []
        else:
            data.wordnet = wordnet_codes.split(' ')
            data.synset = wordnet_service.get_synset_from_key(data.wordnet[0])

        # Get Hypernyms
        data.hypernyms = wordnet_service.get_hypernyms(data)
        senses.append(data)
        

    return senses


def _is_physics_class(themroles:list):
    if not themroles:
        raise ValueError('themroles list empty')

    banned_roles = ['Beneficiary', 'Experiencer', 'Predicate', 'Value']
    banned_selrests = ['organization', 'currency', 'animate', 'human']
    
    for role in themroles:
        if role['type'] in banned_roles:
            return False

        if role['modifiers']:
            for modifier in role['modifiers']:
                if modifier['type'] in banned_selrests:
                    return False
    return True

def _get_themroles_for_class_id(class_id:str, fuse = 0):
    assert fuse < 50

    themroles = vb.themroles(class_id)
    assert type(themroles) == list
    
    id_components = vb.shortid(class_id).split('-')
    if len(id_components) == 1:
        return themroles
    parent_id = '-'.join(id_components[0:-1])

    themroles = themroles + _get_themroles_for_class_id(parent_id, fuse + 1)

    #TODO: need to actually override themroles from superclasses if there's a clash
    # themrole_types = list(map(lambda role: role['type'], themroles))
    # assert len(themrole_types) == len(set(themrole_types))
        
    return themroles


if __name__ == '__main__':
    is_physics_verb('list')

class NotInVerbNetException(Exception):
    pass