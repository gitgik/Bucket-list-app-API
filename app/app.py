from flask.ext.api import FlaskAPI
from flask import request
from models import db, BucketList, BucketListItem
from flask.ext.api.exceptions import \
    AuthenticationFailed, NotFound, ParserError, NotAcceptable
from exceptions.exc import CredentialsRequired
import auth

def create_app(module='config.DevelopmentConfig'):
    """ Wrap the routes into one exportable method """
    app = FlaskAPI(__name__)
    # Object-based configuration 
    app.config.from_object(module)
    db.init_app(app)

    # routes go here

