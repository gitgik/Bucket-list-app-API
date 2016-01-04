import os
import tempfile


class BaseConfig(object):
    """ Base configuration from which other 
        inherit from: defines available endpoints
    """
    DEBUG = False
    TESTING = False
    DATABASE_URL = 'sqlite://:memory'
    AVAILABLE_ENDPOINTS = [
        ("POST /auth/login/", {"PUBLIC_ACCESS": True}),
        ("GET /auth/logout/", {"PUBLIC_ACCESS": False}),
        ("POST /bucketlists/", {"PUBLIC_ACCESS": False}),
        ("GET /bucketlists/", {"PUBLIC_ACCESS": False}),
        ("GET /bucketlists/<id>/", {"PUBLIC_ACCESS": False}),
        ("PUT /bucketlists/<id>/", {"PUBLIC_ACCESS": False}),
        ("DELETE /bucketlists/<id>/", {"PUBLIC_ACCESS": False}),
        ("POST /bucketlists/<id>/items/", {"PUBLIC_ACCESS": False}),
        ("PUT /bucketlists/<id>/items/<item_id>", {"PUBLIC_ACCESS": False}),
        ("DELETE /bucketlists/<id>/items/<item_id>", {"PUBLIC_ACCESS": False}),
    ]


class DevelopmentConfig(BaseConfig):
    """ Sets config for development """
    DEBUG = True
    TESTING = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(BASEDIR,'bucketlist.sqlite')
    SECRET_KEY = 'secret'


class TestingConfig(BaseConfig):
    """ Sets config for testing """
    DEBUG = False
    TESTING = True
    DB_FD, DATABASE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(DATABASE)

class ProductionConfig(BaseConfig):
    """ Sets config for production """
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')

