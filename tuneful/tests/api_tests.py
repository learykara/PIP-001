import unittest
import os
import shutil
import json
from urlparse import urlparse
from StringIO import StringIO

import sys; print sys.modules.keys()

os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful.models import File, Song
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session


class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())

    def seed_db(self):
        """Seed the database with songs and files"""
        for x in range(3):
            file = File(filename='test_song_{}.mp3'.format(x + 1)).save()
            Song(file_id=file.id).save()

    def test_get_all_songs(self):
        # Test with no songs
        response = self.client.get('/api/songs')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

        # Seed database and test for songs
        self.seed_db()

        response = self.client.get('/api/songs')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data)
        self.assertEqual(len(data), 3)

        song = data[0]
        self.assertEqual(song.get('file').get('name'), 'test_song_1.mp3')

    def test_delete_song(self):
        """Delete a song that may or may not exist in database"""

        # Test for song that doesn't exist
        response = self.client.delete('/api/songs/1')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, '')

        self.seed_db()
        num_songs = len(session.query(Song).all())
        response = self.client.delete('/api/songs/1')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, '')
        self.assertEqual(len(session.query(Song).all()), num_songs - 1)

    def test_update_song_existing(self):
        """Update the filename of a song that exists in the db"""
        self.seed_db()
        num_songs = len(session.query(Song).all())

        response = self.client.put(
            '/api/songs/1', data=json.dumps({'filename': 'new_file_name.mp3'}),
            headers={'Content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        song = json.loads(response.data)
        self.assertEqual(song.get('file').get('name'), 'new_file_name.mp3')
        self.assertEqual(len(session.query(Song).all()), num_songs)

    def test_update_song_nonexisting(self):
        """Update the filename of a song that doesn't exist in the db.
        Check that the song has been added to the db."""
        self.assertEqual(len(session.query(Song).all()), 0)
        response = self.client.put(
            '/api/songs/1', data=json.dumps({'filename': 'new_file_name.mp3'}),
            headers={'Content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        song = json.loads(response.data)
        self.assertEqual(song.get('file').get('name'), 'new_file_name.mp3')
        self.assertEqual(len(session.query(Song).all()), 1)

    def test_get_uploaded_file(self):
        path = upload_path('test.txt')
        with open(path, 'w') as f:
            f.write('File contents')

        response = self.client.get('/uploads/test.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/plain')
        self.assertEqual(response.data, 'File contents')

    def test_file_upload(self):
        data = {
            'file': (StringIO('File contents'), 'test.txt')
        }

        response = self.client.post(
            '/api/files', data=data, content_type='multipart/form-data',
            headers=[('Accept', 'application/json')])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data)
        self.assertEqual(urlparse(data.get('path')).path, '/uploads/test.txt')

        path = upload_path('test.txt')
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            contents = f.read()
        self.assertEqual(contents, 'File contents')
