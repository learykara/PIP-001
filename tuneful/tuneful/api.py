import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

import decorators
from models import Song, File
from tuneful import app
from database import session
from utils import upload_path


MIMETYPE = 'application/json'


@app.route('/api/songs', methods=['GET'])
def get_songs():
    """Return a json object of all the songs in the db"""
    songs = [song.to_dict() for song in session.query(Song).all()]
    return Response(json.dumps(songs), 200, mimetype=MIMETYPE)
