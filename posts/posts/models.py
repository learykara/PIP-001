import json

from sqlalchemy import Column, Integer, String

from database import Base, session


class ModelUtils(object):
    def save(self):
        session.add(self)
        session.commit()
        return self

    def remove(self):
        session.delete(self)
        session.commit()
        return True


class Post(Base, ModelUtils):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    body = Column(String(1024))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body
        }

    def update(self, value_dict):
        value_dict = json.loads(value_dict)
        self.title = value_dict.get('title', self.title)
        self.body = value_dict.get('body', self.body)
