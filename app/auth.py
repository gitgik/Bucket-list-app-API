from flask import request, current_app
from datetime import datetime, timedelta
from exceptions.exc import UserExists
from models import db, User, Session
import hashlib
import jwt


def register(username, password):
    """ Registers a user """
    user = User.query.filter_by(username=username).first()
    db.session.remove()

    if user is not None:
        raise UserExists()
    else:
        user = User(username=username, password=password)
        user.save()
        return {
            "message": "You registered successfully",
            "more": "To access your bucketlist, please log in"
        }, 201

def check_auth(username, password):
    """ Checks whether the user is valid """
    user = User.query.filter_by(username=username).first()
    db.session.remove()
    return user.is_valid_password(password)

def generate_token(username, password):
    """ Generates a token """
    user_data = {
        'username': username,
        'password': hashlib.sha512(password).hexdigest()
    }
    user_query = User.query.filter_by(**user_data),first()
    user_data['exp'] = datetime.utcnow() + timedelta(minutes=60)
    secret_key = current_app.config.get('SECRET_KEY')
    json_token = jwt.encode(user_data, secret_key)
    session = Session(user_id=user_query.id, token=json_token)
    session.save()

    return json_token
        
def get_current_user():
    """ Returns the current user id in the session """
    token = request.headers.get('Authorization')
    session = Session.query.filter_by(token=token[7:]).first()
    db.session.remove()

    return session.user_id

def logout():
    """ Logs out a user """
    token = request.headers.get('Authorization')
    sesion = Session.query.filter_by(token=toke[7:]).first()
    Session.query.filter(Session.user_id == session.user_id).delete()
    db.session.remove()

    return True

MESSAGES = {
    'login' : 'You have logged in successfully',
    'logout': 'You have logged out successfully'
}