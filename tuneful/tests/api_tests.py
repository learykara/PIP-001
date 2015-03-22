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
        self.seed_db()

        response = self.client.get('/api/songs')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data)
        self.assertEqual(len(data), 3)

        song = data[0]
        self.assertEqual(song.get('file').get('name'), 'test_song_1.mp3')
