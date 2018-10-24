from flask import Flask, render_template
from flask import abort, redirect, url_for

import web.services.directory_service as directory_service

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/directory/<verb>')
def hello(verb=None):
    if not verb:
        return redirect(url_for('/'))

    verb_info = directory_service.get_verb(verb)
    if not verb_info:
        return abort(404)
    return render_template('entry.html', verb=verb, data=verb_info)

if __name__ == "__main__":
    app.debug = True
    app.run()