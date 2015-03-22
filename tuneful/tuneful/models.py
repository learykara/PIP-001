import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, engine, session


class ModelUtils(object):

    def save(self):
        session.add(self)
        session.commit()
        return self

    def delete(self):
        session.delete(self)
        session.commit()
        return True


class Song(Base, ModelUtils):
    """Models a song"""
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'file': {
                'id': self.file_id,
                'name': self.file.filename
            }
        }


class File(Base, ModelUtils):
    """Models a file"""
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    filename = Column(String(128))
    song = relationship('Song', backref='file')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


Base.metadata.create_all(engine)
