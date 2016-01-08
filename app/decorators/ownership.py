import jwt
from ..models import db, User, Session, BucketList, BucketListItem
from flask import request, current_app
from flask.ext.sqlalchemy import sqlalchemy
from functools import wraps
from flask.ext.api.exceptions import \
    AuthenticationFailed, PermissionDenied, NotFound
from ..exceptions.handler import ValidationError
from ..auth import get_current_user


def owned_by_user(f):
    """ Force a model to be owned by a user """
    @wraps(f)
    def decorated(*args, **kwargs):
        bucketlist_id = kwargs.get('id')
        bucketlist = BucketList.query.get(int(bucketlist_id))
        db.session.remove()

        if bucketlist.created_by != get_current_user():
            raise PermissionDenied()
        return f(*args, **kwargs)
    return decorated


def auth_required(f):
    """ Force client to authenticate before getting access """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            jwt_token = request.headers.get('Authorization')
            secret_key = current_app.config.get('SECRET_KEY')

            try:
                decoded_jwt = jwt.decode(jwt_token[7:], secret_key)
            except jwt.ExpiredSignatureError:
                raise PermissionDenied(
                    'Your token has expired! Please login again')
            User.query.filter_by(
                username=decoded_jwt['username'],
                password=decoded_jwt['password']).one()
            if not Session.query.filter_by(token=jwt_token[7:]):
                raise AuthenticationFailed()

        except (sqlalchemy.orm.exc.MultipleResultsFound,
                sqlalchemy.orm.exc.NoResultFound):
            raise ValidationError()
        return f(*args, **kwargs)
    return decorated


def owned_by_bucketlist(f):
    """ Force an item to be owned by a BucketList """
    @wraps(f)
    def decorated(*args, **kwargs):
        bucketlist_id = kwargs.get('id')
        bucketlistitem_id = kwargs.get('item_id')
        bucketlist_item = BucketListItem.query.get(int(bucketlistitem_id))
        db.session.remove()
        if bucketlist_item:
            try:
                assert bucketlist_item.bucketlist_id == int(bucketlist_id)
            except:
                raise NotFound()
        kwargs['item'] = bucketlist_item
        return f(*args, **kwargs)
    return decorated
