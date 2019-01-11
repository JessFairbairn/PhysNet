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
    return render_template('entry.html', verb=verb, data=verb_info)

@app.route('/synsets/<set_name>')
def synset(set_name:str):
    verbs_in_set = directory_service.get_verbs_in_synset(set_name)
    return render_template('synset.html', set_name=set_name, verbs_in_set=verbs_in_set)

@app.route('/svg/<verb>')
def get_condep_diagram(verb:str):
    if not svg_service.SVGService.diagram_exists(verb):
        verb_info = directory_service.get_verb(verb)
        
        if not verb_info:
            return abort(404)

        svg_service.SVGService.create_diagram(verb, verb_info.condep)

    return redirect(url_for('static', filename='cd-diagrams/'+ verb + '.svg'))

if __name__ == "__main__":
    app.debug = True
    app.run()