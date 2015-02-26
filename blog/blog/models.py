import datetime

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from flask.ext.login import UserMixin

from database import Base, engine, session


class ModelUtils(object):
    def save(self):
        """Convenience instance method for saving to db"""
        session.add(self)
        session.commit()
        return self

    def remove(self):
        """Convenience instance method for removing from db"""
        session.delete(self)
        session.commit()
        return True


class Post(Base, ModelUtils):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now())
    author_id = Column(Integer, ForeignKey('users.id'))


class User(Base, UserMixin, ModelUtils):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    posts = relationship('Post', backref='author')


Base.metadata.create_all(engine)
