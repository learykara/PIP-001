import os

from flask.ext.script import Manager

from blog import app
from blog.database import session
from blog.models import Post


manager = Manager(app)


@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(port=port)


@manager.command
def seed():
    content = (
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do"
        " eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut"
        " enim ad minim veniam, quis nostrud exercitation ullamco laboris"
        " nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor"
        " in reprehenderit in voluptate velit esse cillum dolore eu fugiat"
        " nulla pariatur. Excepteur sint occaecat cupidatat non proident,"
        " sunt in culpa qui officia deserunt mollit anim id est laborum.""")

    for i in range(25):
        post = Post(
            title="Test Post #{}".format(i),
            content=content
        )
        session.add(post)
    session.commit()


if __name__ == '__main__':
    manager.run()