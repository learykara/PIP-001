import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError

import decorators
from posts import app
from posts.models import Post
from database import session


@app.route('/api/posts', methods=['GET'])
@decorators.accept('application/json')
def get_all_posts():
    """Get a list of posts"""
    posts = session.query(Post).all()
    data = json.dumps([post.to_dict() for post in posts])
    return Response(data, 200, mimetype='application/json')


@app.route('/api/posts/<int:id>', methods=['GET'])
@decorators.accept('application/json')
def get_single_post(id): # same name as above?
    """Single post endpoint"""
    post = session.query(Post).get(id)

    if not post:
        message = 'Could not find post with id {}'.format(id)
        data = json.dumps({'message': message})
        return Response(data, 404, mimetype='application/json')

    data = json.dumps(post.to_dict())
    return Response(data, 200, mimetype='application/json')
