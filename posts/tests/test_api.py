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
        self.headers = [('Accept', 'application/json')]

    def tearDown(self):
        session.close()
        Base.metadata.drop_all(engine)

    def seed_db(self):
        Post(title='Post with bells', body='Just a test').save()
        Post(title='Post with whistles', body='Still a test').save()
        Post(
            title='Post with bells and whistles',
            body='All of the tests.').save()

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
        self.assertEqual(len(data), 3)

        post_a = data[0]
        self.assertEqual(post_a.get('title'), 'Post with bells')
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
        self.assertEqual(post.get('title'), 'Post with whistles')
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

    def test_delete_post(self):
        """Delete a single post that exists in the db"""
        self.seed_db()

        response = self.client.delete('/api/posts/2', headers=self.headers)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.mimetype, 'application/json')

    def test_delete_nonexistent_post(self):
        """Attempt to delete a single post that doesn't exist"""
        response = self.client.delete('/api/posts/1', headers=self.headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data)

        self.assertEqual(
            data.get('message'), 'Could not delete post with id 1')

    def test_get_posts_with_title(self):
        """Filtering posts by title"""
        self.seed_db()

        response = self.client.get(
            '/api/posts?title_like=whistles', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

        posts = json.loads(response.data)
        self.assertEqual(len(posts), 2)

        post = posts[0]
        self.assertEqual(post.get('title'), 'Post with whistles')
        self.assertEqual(post.get('body'), 'Still a test')

        post = posts[1]
        self.assertEqual(post.get('title'), 'Post with bells and whistles')
        self.assertEqual(post.get('body'), 'All of the tests.')

    def test_get_posts_with_body(self):
        """Filtering posts by body"""
        self.seed_db()

        response = self.client.get(
            '/api/posts?body_like=tests', headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

        posts = json.loads(response.data)
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.get('title'), 'Post with bells and whistles')

    def test_get_posts_with_title_and_body(self):
        """Filtering by title and body"""
        self.seed_db()

        response = self.client.get(
            '/api/posts?title_like=whistles&body_like=still',
            headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

        posts = json.loads(response.data)
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.get('title'), 'Post with whistles')
        self.assertEqual(post.get('body'), 'Still a test')

    def test_post_post(self):
        """Posting a new post"""
        data = {
            'title': 'Example post',
            'body': 'Just a test'
        }

        response = self.client.post(
            '/api/posts', data=json.dumps(data),
            content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual(
            urlparse(response.headers.get('Location')).path, '/api/posts/1')

        response_data = json.loads(response.data)
        self.assertEqual(response_data.get('id'), 1)
        self.assertEqual(response_data.get('title'), data.get('title'))
        self.assertEqual(response_data.get('body'), data.get('body'))

        posts = session.query(Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, data.get('title'))
        self.assertEqual(post.body, data.get('body'))

    def test_unsupported_mimetype(self):
        """Send data of incorrect type to POST endpoint"""
        data = '<xml></xml>'
        response = self.client.post(
            '/api/posts', data=json.dumps(data),
            content_type='application/xml', headers=self.headers)

        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.mimetype, 'application/json')

        data = json.loads(response.data)
        self.assertEqual(
            data.get('message'), 'Request must contain application/json data')

    def test_invalid_data(self):
        """Posting a post with invalid body"""
        data = {
            'title': 'Example Post',
            'body': 32
        }

        response = self.client.post(
            '/api/posts', data=json.dumps(data),
            content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 422)

        data = json.loads(response.data)
        self.assertEqual(data.get('message'), "32 is not of type 'string'")

    def test_missing_data(self):
        """Post a post with a missing body"""
        data = {
            'title': 'Example Post'
        }

        response = self.client.post(
            '/api/posts', data=json.dumps(data),
            content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 422)

        data = json.loads(response.data)
        self.assertEqual(data.get('message'), "'body' is a required property")

    def test_post_put(self):
        """Update a single post"""
        self.seed_db()
        data = {
            'title': 'Updated title',
            'body': 'Updated body'
        }

        response = self.client.put(
            '/api/posts/1', data=json.dumps(data),
            content_type='application/json', headers=self.headers)

        self.assertEqual(response.status_code, 201)

        response_data = json.loads(response.data)
        self.assertEqual(response_data.get('title'), data.get('title'))
        self.assertEqual(response_data.get('body'), data.get('body'))


if __name__ == '__main__':
    unittest.main()
