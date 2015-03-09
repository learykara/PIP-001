from flask import (
    render_template, request, redirect, url_for, flash)
from flask.ext.login import (
    login_user, login_required, current_user, logout_user)
from werkzeug.security import check_password_hash

from blog import app
from database import session
from models import Post, User


def editable(post_id):
    """Check if the current user is the author of a post"""
    post = session.query(Post).filter_by(id=post_id).first()
    return post in current_user.posts


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect username or password', 'danger')
        return redirect(url_for('login_get'))

    login_user(user)
    return redirect(request.args.get('next') or url_for('posts'))


@app.route('/logout', methods=['POST'])
@login_required
def logout_post():
    logout_user()
    return redirect(url_for('posts'))


def paginate(page_index, paginate_by=10):
    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    return [start, end, total_pages]


@app.route('/')
@app.route('/page/<int:page>')
def posts(page=1, paginate_by=10):
    page_index = page - 1
    [start, end, total_pages] = paginate(page_index)

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    return render_template(
        'posts.html',
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages,
        user=current_user
    )


@app.route('/posts/add', methods=["GET"])
@login_required
def add_post_get():
    return render_template('add_post.html')


@app.route('/posts/add', methods=["POST"])
@login_required
def add_post_post():
    post = Post(
        title=request.form['title'],
        content=request.form['content'],
        author=current_user
    )
    session.add(post)
    session.commit()
    flash('Post successfully added', 'success')
    return redirect(url_for('posts'))


@app.route('/posts/<post_id>')
def view_post(post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('posts'))
    return render_template(
        'view_post.html',
        post=post,
        user=current_user
    )


@app.route('/posts/<post_id>/edit', methods=["GET"])
@login_required
def edit_post_get(post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('posts'))
    if not editable(post_id):
        flash('You are not authorized to edit this post', 'danger')
        return redirect(url_for('posts'))
    return render_template(
        'edit_post.html',
        post=post
    )


@app.route('/posts/<post_id>/edit', methods=["POST"])
@login_required
def edit_post_post(post_id):
    if not editable(post_id):
        flash('You are not authorized to edit this post', 'danger')
        return redirect(url_for('posts'))
    title = request.form['title']
    content = request.form['content']
    session.query(Post).filter_by(id=post_id).update({
        'title': title, 'content': content})
    session.commit()
    flash('Post successfully updated', 'success')
    return redirect(url_for('view_post', post_id=post_id))


@app.route('/posts/<post_id>/delete', methods=["GET"])
@login_required
def delete_post_get(post_id):
    if not editable(post_id):
        flash('You are not authorized to delete this post', 'danger')
        return redirect(url_for('posts'))
    post = session.query(Post).filter_by(id=post_id).first()
    return render_template('delete_post.html', post=post)


@app.route('/posts/<post_id>/delete', methods=["POST"])
@login_required
def delete_post_post(post_id):
    if not editable(post_id):
        flash('You are not authorized to delete this post', 'danger')
        return redirect(url_for('posts'))
    post = session.query(Post).filter_by(id=post_id).first()
    session.delete(post)
    session.commit()
    flash('Post successfully deleted', 'success')
    return redirect(url_for('posts'))


@app.route('/posts/my', methods=["GET"])
@login_required
def see_user_posts():
    posts = session.query(Post).filter_by(author_id=current_user.id)
    posts = posts.order_by(Post.datetime.desc())
    return render_template('posts.html', posts=posts, user=current_user)
