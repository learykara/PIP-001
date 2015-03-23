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


@app.route('/api/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    to_delete = session.query(Song).get(song_id)
    if to_delete:
        to_delete.delete()
    return Response([], 204, mimetype=MIMETYPE)


@app.route('/api/songs/<int:song_id>', methods=['PUT'])
def put_song(song_id):
    """Update the filename of a song. If the song doesn't exist, create it"""
    song = session.query(Song).get(song_id)
    filename = request.json.get('filename')
    if not song:
        file = File(filename=filename).save()
        song = Song(file_id=file.id).save()
    else:
        song.file.filename = filename
        song.save()
    return Response(json.dumps(song.to_dict()), 201, mimetype=MIMETYPE)
