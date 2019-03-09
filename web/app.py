import os
import sys

from flask import Flask, render_template
from flask import abort, redirect, url_for

# Hack to import condep
# TODO: add condep to pip
dir_path = os.path.dirname(os.path.realpath(__file__))
slash_positions = ([pos for pos, char in enumerate(dir_path) if char == '/'])
sys.path.append(dir_path[0:slash_positions[-1]] + '/ConDep')

# pylint: disable=E0401
import condep
try:
    from .services import directory_service
except ImportError:
    from services import directory_service

try:
    from .services import svg_service
except ImportError:
    from services import svg_service

try:
    from .services import condep_service
except ImportError:
    from services import condep_service



app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('directory'))
    # return render_template('home.html')

@app.route('/directory/')
def directory():
    verb_list = directory_service.get_verb_list()
    verb_directory = directory_service.get_verb_details()
    return render_template('directory.html', verb_list=verb_list, directory = verb_directory)

@app.route('/directory/<verb>')
def verb_entry(verb:str):

    verb_info = directory_service.get_verb(verb)
    if not verb_info:
        return abort(404)

    # condep = condep_service.get_condep_for_verb(verb)
    # if condep:
    #     verb_info.condep = condep

    return render_template('entry.html', verb=verb, data=verb_info)

@app.route('/synsets')
def synset_list():
    synsets = directory_service.get_list_of_synsets()
    return render_template('synset_list.html', synsets=synsets)

@app.route('/synsets/<set_name>')
def synset(set_name:str):
    verbs_in_set = directory_service.calculate_verbs_in_synsets(set_name)
    hyponyms = directory_service.get_hyponyms_of_synset(set_name)
    return render_template('synset.html', set_name=set_name, verbs_in_set=verbs_in_set, hyponyms=hyponyms)

@app.route('/svg/<verb>')
def get_condep_diagram(verb:str):
    if not svg_service.SVGService.diagram_exists(verb):
        condep = condep_service.get_condep_for_verb(verb)
        
        if not condep:
            return abort(404)

        svg_service.SVGService.create_diagram(verb, condep)

    return redirect(url_for('static', filename='cd-diagrams/'+ verb + '.svg'))

@app.route('/svg/synset/<path:synpath>')
def get_condep_diagram_for_synset(synpath:str):

    synset = synpath.split('/')[0]
    try:
        verb = synpath.split('/')[1]
    except IndexError:
        verb = None

    if not svg_service.SVGService.diagram_exists(synset):
        condep = condep_service.get_condep_for_synset(synset, verb)
        
        if not condep:
            return abort(404)

        svg_service.SVGService.create_diagram(synset, condep)

    return redirect(url_for('static', filename='cd-diagrams/'+ synset + '.svg'))

if __name__ == "__main__":
    app.debug = True
    app.run()