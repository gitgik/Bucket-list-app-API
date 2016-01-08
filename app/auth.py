from flask import request, current_app
from datetime import datetime, timedelta
from exceptions.handler import UserAlreadyExists
from models import db, User, Session
import hashlib
import jwt


def register(username, password):
    """ Registers a user """
    user = User.query.filter_by(username=username).first()
    db.session.remove()

    if user is not None:
        raise UserAlreadyExists()
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
    return user.password_is_valid(password)


def generate_token(username, password):
    """ Generates a token """
    user = {
        "username": username,
        "password": hashlib.sha512(password).hexdigest()
    }
    user_results = User.query.filter_by(**user).first()
    user['exp'] = datetime.utcnow() + timedelta(minutes=60)
    secret_key = current_app.config.get('SECRET_KEY')
    jwt_string = jwt.encode(user, secret_key)
    session = Session(user_id=user_results.id, token=jwt_string)
    session.save()
    return jwt_string


def get_current_user():
    """ Returns the current user id in the session """
    token = request.headers.get('Authorization')
    session = Session.query.filter_by(token=token[7:]).first()
    db.session.remove()
    return session.user_id


def logout():
    """ Logs out a user """
    token = request.headers.get('Authorization')
    session = Session.query.filter_by(token=token[7:]).first()
    Session.query.filter(Session.user_id == session.user_id).delete()
    db.session.remove()
    return True

SERVICE_MESSAGES = {
    'login': 'You have logged in successfully',
    'logout': 'You have logged out successfully'
}
