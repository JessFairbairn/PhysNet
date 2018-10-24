from flask import Flask, render_template
from flask import abort, redirect, url_for

import web.services.directory_service as directory_service

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