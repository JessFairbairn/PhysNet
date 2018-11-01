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

from web.services import directory_service 


app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('directory'))
    # return render_template('home.html')

@app.route('/directory/')
def directory():
    verb_list = directory_service.get_verb_list()
    return render_template('directory.html', verb_list=verb_list)

@app.route('/directory/<verb>')
def verb_entry(verb:str):

    verb_info = directory_service.get_verb(verb)
    if not verb_info:
        return abort(404)
    return render_template('entry.html', verb=verb, data=verb_info)

if __name__ == "__main__":
    app.debug = True
    app.run()