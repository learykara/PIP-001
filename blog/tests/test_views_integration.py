import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

os.environ['CONFIG_PATH'] = 'blog.config.TestingConfig'

from blog import app, models
from blog.database import Base, engine, session


class TestViews(unittest.TestCase):
    def setUp(self):
        """Test setup"""
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create a test user
        self.user = models.User(
            name='Alice', email='alice@example.com',
            password=generate_password_hash('test')).save()

    def tearDown(self):
        """Test teardown"""
        session.close()
        Base.metadata.drop_all(engine)

    def simulate_login(self):
        """Mimic flask-login"""
        with self.client.session_transaction() as http_session:
            http_session['user_id'] = str(self.user.id)
            http_session['_fresh'] = True

    def test_add_post(self):
        self.simulate_login()

        response = self.client.post(
            '/posts/add', data={
                'title': 'Test Post', 'content': 'Test content'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/')
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'Test content')
        self.assertEqual(post.author, self.user)

    def add_post(self):
        """Add a test post to the db."""
        self.client.post('/posts/add', data={
            'title': 'Test Post', 'content': 'Test content'})

    def test_edit_post_authorized(self):
        """Test that a post that is edited is properly updated"""
        self.simulate_login()
        self.add_post()
        post_id = session.query(models.Post).first().id
        response = self.client.post('/posts/{}/edit'.format(post_id), data={
            'title': 'Updated title', 'content': 'Updated content'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            urlparse(response.location).path, '/posts/{}'.format(post_id))
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, 'Updated title')
        self.assertEqual(post.content, 'Updated content')
        self.assertEqual(post.author, self.user)

    def test_edit_post_unauthorized(self):
        """Test that a post cannot be edited by anyone but the author"""
        post = models.Post(
            title='Test Post', content='Test Content', author=self.user).save()
        post_id = session.query(models.Post).first().id

        response = self.client.get('/posts/{}/edit'.format(post_id))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/login')

        response = self.client.post('/posts/{}/edit'.format(post_id), data={
            'title': 'Updated title', 'content': 'Updated content'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/login')
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'Test Content')
        self.assertEqual(post.author, self.user)

    def test_delete_post_authorized(self):
        """Test that a deleted post is removed from the db"""
        self.simulate_login()
        self.add_post()
        post_id = session.query(models.Post).first().id

        response = self.client.get('/posts/{}/delete'.format(post_id))
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/posts/{}/delete'.format(post_id))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/')

    def test_delete_post_unauthorized(self):
        """Test that a post can only be deleted by its author"""
        models.Post(
            title='Test Post', content='Test Content', author=self.user).save()
        post_id = session.query(models.Post).first().id

        response = self.client.get('/posts/{}/delete'.format(post_id))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/login')

        response = self.client.post('/posts/{}/delete'.format(post_id))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/login')

    def tests_my_posts(self):
        """Test that visiting /posts/my shows the posts of the current user"""
        self.simulate_login()
        self.add_post()

        response = self.client.get('/posts/my')
        self.assertEqual(response.status_code, 200)

    def test_not_my_posts(self):
        """Test that visiting /posts/my while not logged in redirects
        to the login page"""
        models.Post(
            title='Test Post', content='Test Content', author=self.user).save()

        response = self.client.get('/posts/my')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/login')


if __name__ == '__main__':
    unittest.main()
