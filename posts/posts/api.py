import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError
from sqlalchemy import func

import decorators
from posts import app
from posts.models import Post
from database import session


mimetype = 'application/json'


# JSON Schema describing the structure of a post
post_schema = {
    'properties': {
        'title': {'type': 'string'},
        'body': {'type': 'string'}
    },
    'required': ['title', 'body']
}


@app.route('/api/posts', methods=['GET'])
@decorators.accept(mimetype)
def get_all_posts():
    """Get a list of posts"""
    posts = session.query(Post)
    title_like = request.args.get('title_like')
    body_like = request.args.get('body_like')

    if title_like:
        posts = posts.filter(
            func.lower(Post.title).contains(title_like.lower()))
    if body_like:
        posts = posts.filter(
            func.lower(Post.body).contains(body_like.lower()))
    posts = posts.all()

    data = json.dumps([post.to_dict() for post in posts])
    return Response(data, 200, mimetype=mimetype)


@app.route('/api/posts/<int:id>', methods=['GET'])
@decorators.accept(mimetype)
def get_single_post(id):
    """Single post endpoint"""
    post = session.query(Post).get(id)

    if not post:
        message = 'Could not find post with id {}'.format(id)
        data = json.dumps({'message': message})
        return Response(data, 404, mimetype=mimetype)

    data = json.dumps(post.to_dict())
    return Response(data, 200, mimetype=mimetype)


@app.route('/api/posts', methods=['POST'])
@decorators.accept(mimetype)
@decorators.require(mimetype)
def posts_post():
    """Add a new post"""
    data = request.json

    # Validate data
    try:
        validate(data, post_schema)
    except ValidationError as error:
        data = {'message': error.message}
        return Response(json.dumps(data), 422, mimetype='application/json')

    post = Post(title=data.get('title'), body=data.get('body')).save()

    # Return 201 Created, containing post as JSON
    data = json.dumps(post.to_dict())
    headers = {'Location': url_for('get_single_post', id=post.id)}
    return Response(data, 201, headers=headers, mimetype=mimetype)


@app.route('/api/posts/<int:id>', methods=['PUT'])
@decorators.accept(mimetype)
@decorators.require(mimetype)
def posts_put(id):
    """Edit a single post with ID `id`"""
    post = session.query(Post).get(id)
    data = request.json

    if not post:
        message = 'Could not edit post with id {}'.format(id)
        data = json.dumps({'message': message})
        return Response(data, 404, mimetype=mimetype)

    # Validate data
    try:
        validate(data, post_schema)
    except ValidationError as error:
        data = {'message': error.message}
        return Response(data, 422, mimetype='application/json')

    post.update(json.dumps(data))

    # Return 201 Created, containing updated post as JSON
    data = json.dumps(post.to_dict())
    headers = {'Location': url_for('get_single_post', id=post.id)}
    return Response(data, 201, headers=headers, mimetype=mimetype)


@app.route('/api/posts/<int:id>', methods=['DELETE'])
@decorators.accept(mimetype)
def delete_post(id):
    """Delete a single post with ID `id`"""
    post = session.query(Post).get(id)

    if not post:
        message = 'Could not delete post with id {}'.format(id)
        data = json.dumps({'message': message})
        return Response(data, 404, mimetype=mimetype)

    post.remove()
    return Response([], 204, mimetype=mimetype)
