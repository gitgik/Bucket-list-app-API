import os
import tempfile


class BaseConfig(object):
    """ Base configuration from which others
        inherit from: defines available endpoints
    """
    DEBUG = False
    TESTING = False
    DATABASE_URL = 'sqlite://:memory:'
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
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '1509717492663327',
            'secret': 'd6ef23f9617a2789e038833f4395391f'
        }
    }
    SECRET_KEY = 'secret'


class DevelopmentConfig(BaseConfig):
    """ Sets config for development """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(BASE_DIR, 'bucketlist.sqlite')
    SECRET_KEY = 'secret'


class TestingConfig(BaseConfig):
    """ Sets config for testing """
    TESTING = True
    DB_FD, DATABASE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(DATABASE)
    SECRET_KEY = 'secret'


class ProductionConfig(BaseConfig):
    """ Sets config for production """
    TESTING = False
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(BASE_DIR, 'bucketlist.sqlite')
    SECRET_KEY = 'a_bucketlist_secret'
