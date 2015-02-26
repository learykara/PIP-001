import os
from getpass import getpass

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash

from blog import app
from blog.database import session, Base
from blog.models import Post, User


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
        Post(
            title="Test Post #{}".format(i),
            content=content
        ).save()


@manager.command
def adduser():
    name = raw_input('Name: ')
    email = raw_input('Email: ')
    if session.query(User).filter_by(email=email).first():
        print 'User with that email already exists.'
        return

    password = ''
    password_2 = ''
    while not (password and password_2) or password != password_2:
        password = getpass('Password: ')
        password_2 = getpass('Re-enter password: ')
    User(
        name=name,
        email=email,
        password=generate_password_hash(password)
    ).save()


class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata


migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
