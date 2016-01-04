from flask.ext.api import FlaskAPI
from flask import request
from models import db, BucketList, BucketListItem
from flask.ext.api.exceptions import \
    AuthenticationFailed, NotFound, ParseError, NotAcceptable
from exceptions.handler import CredentialsRequired
import auth


def create_app(module='config.DevelopmentConfig'):
    """ Wrap the routes into one exportable method """
    app = FlaskAPI(__name__)
    # Object-based configuration
    app.config.from_object(module)
    db.init_app(app)

    # routes go here
    @app.route('/auth/register', methods=['GET', 'POST'])
    def register():
        """ return JSON response """
        if request.method == 'GET':
            return {
                'message': 'Welcome to the BucketList service',
                'more': 'Please make a POST /register \
                 with username and password'
            }, 200
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            if username and password:
                return auth.register(username, password)
            else:
                raise ParseError()

