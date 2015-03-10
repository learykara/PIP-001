import unittest
import os
import json
from urlparse import urlparse

os.environ['CONFIG_PATH'] = 'posts.config.TestingConfig'

from posts import app
from posts.database import Base, engine, session
from posts.models import Post


class TestAPI(unittest.TestCase):
    """Tests for the posts API"""

    def setUp(self):
        self.client = app.test_client()
        Base.metadata.create_all(engine)

    def tearDown(self):
        session.close()
        Base.metadata.drop_all(engine)

    def seed_db(self):
        Post(title='Post A', body='Just a test').save()
        Post(title='Post B', body='Still a test').save()

    @property
    def headers(self):
        return [('Accept', 'application/json')]

    def test_get_empty_posts(self):
        """Get posts from an empty database"""
        response = self.client.get('/api/posts', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data)
        self.assertEqual(data, [])

    def test_get_posts(self):
        """Get posts from a populated database"""
        self.seed_db()

        response = self.client.get('/api/posts', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

        post_a = data[0]
        self.assertEqual(post_a.get('title'), 'Post A')
        self.assertEqual(post_a.get('body'), 'Just a test')

    def test_get_single_post(self):
        """Get a single post from populated db"""
        self.seed_db()
        post_b = session.query(Post).get(2)

        response = self.client.get(
            '/api/posts/{}'.format(post_b.id), headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

        post = json.loads(response.data)
        self.assertEqual(post.get('title'), 'Post B')
        self.assertEqual(post.get('body'), 'Still a test')

    def test_get_nonexistent_post(self):
        """Get a single post which doesn't exist"""
        response = self.client.get('/api/posts/1', headers=self.headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data)
        self.assertEqual(data.get('message'), 'Could not find post with id 1')

    def test_unsupported_accept_header(self):
        response = self.client.get(
            '/api/posts', headers=[('Accept', 'application/xml')])

        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data)
        self.assertEqual(
            data.get('message'), 'Request must accept application/json data')


if __name__ == '__main__':
    unittest.main()
