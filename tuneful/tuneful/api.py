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


@app.route('/api/songs', methods=['POST'])
def post_song():
    """Add a new song to the db"""
    file = request.json.get('file')
    if not file:
        data = {'message': 'Could not load data'}
        return Response(json.dumps(data), 404, mimetype=MIMETYPE)

    new_file = File(filename=file.get('name')).save()
    song = Song(file_id=new_file.id).save()

    return Response(json.dumps(song.to_dict()), 201, mimetype=MIMETYPE)


@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(upload_path(), filename)


@app.route('/api/files', methods=['POST'])
@decorators.require('multipart/form-data')
@decorators.accept('application/json')
def file_post():
    file = request.files.get('file')
    if not file:
        data = {'message': 'Could not find file data'}
        return Response(json.dumps(data), 422, mimetype=MIMETYPE)

    filename = secure_filename(file.filename)
    db_file = File(filename=filename).save()
    file.save(upload_path(filename))

    data = db_file.to_dict()
    return Response(json.dumps(data), 201, mimetype=MIMETYPE)
