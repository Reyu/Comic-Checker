import os

import firebase_admin
import flask
import json
from firebase_admin import credentials, firestore
# from lxml import html


cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': os.environ.get('GCP_PROJECT')
    })

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
    print('Fetching comics list')
    db = firestore.client()
    comics_ref = db.collection(u'comics')
    comics = comics_ref.get()

    if request_wants_json(request):
        return (
            json.dumps({doc.id: doc.to_dict() for doc in comics}),  # Body
            200,                                                    # Status
            {'content-type': 'application/json'}                    # Headers
        )

    return (
        "".join(
            ['<a href="{url}">{name}</a><br />'.format(
                    name=doc.id, url=doc.get(u'url')
                ) for doc in comics]
        ),
        200
    )
