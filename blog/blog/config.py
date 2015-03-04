import os


class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://karaleary:karaleary@localhost:5432/blogful"
    DEBUG = True
    SECRET_KEY = 'secret'
    # untrack this file and hard code in secret key


class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://karaleary:karaleary@localhost:5432/blogful-test'
    DEBUG = False
    SECRET_KEY = 'Not secret'
