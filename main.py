import os

import firebase_admin
import flask
import json
from jinja2 import Environment, ChoiceLoader, ModuleLoader, FileSystemLoader
from firebase_admin import credentials, firestore
# from lxml import html


# === Globals ===
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': os.environ.get('GCP_PROJECT')
    })
db = firestore.client()
jinja = Environment(
        loader=ChoiceLoader([
            ModuleLoader(os.path.abspath(os.curdir) + '/jinja.cache'),
            FileSystemLoader(os.path.abspath(os.curdir) + '/templates')
        ]))

# === Helper Functions ===


def request_wants_json(request):
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


# === Entrypoints ===


def list_comics(request: flask.Request):
    """List all registered comics
    Args:
        request: The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any of the values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flsk.make_response>.
    """
    comics_ref = db.collection(u'comics')
    comics = {doc.id: doc.to_dict() for doc in comics_ref.get()}
    response = flask.Response()

    if request_wants_json(request):
        response.content_type = 'application/json'
        response.set_data(json.dumps(comics))
    else:
        template = jinja.get_template('list.jinja2')
        response.set_data(template.render(comics=comics))

    return response
