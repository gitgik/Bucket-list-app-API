from flask_sqlalchemy import sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapper
import hashlib

db = SQLAlchemy()


class Base(db.Model):
    """ Base model from which other models will inherit from """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    
    def save(self):
        """ Save the object instance of the model """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Deletes the object instance of the model """
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        """ Serializes objects to json """
        jsonDict = dict()
        result_list = []
        for propt in mapper(self.__class__).iterate_properties:
            if propt.key == 'user':
                continue
            if propt.key == 'items':
                items = getattr(self, propt.key)
                for item in items:
                    if callable(getattr(item, 'to_json')):
                        result = item.to_json()
                        result_list.append(result)
                        jsonDict[propt.key] = result_list
                        continue

            jsonDict[propt.key] = getattr(self, propt.key)

        return jsonDict


class User(Base):
    """ Maps to users table """
    __tablename__ = 'users'
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    bucketlists = db.relationship(
        'BucketList', order_by='BucketList.id')


class BucketList(Base):
    """ Maps to the bucketlists table """
    __tablename__ = 'bucketlists'
    name       = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    
    user = db.relationship('User')
    items = db.relationship('BucketListItem')

    def __init__(self, creator, name):
        """ Initialize with the creator and name of bucketlist """
        self.created_by = creator
        self.name = name


class Session(Base):
    """ Maps to session table """
    __tablename__ = 'sessions'
    user_id = db.Column(db.Integer)
    token = db.Column(db.String(256))


class BucketListItem(Base):
    """ Maps to BucketList table """
    __tablename__ = 'items'
    name = db.Column(db.String(256), nullable=False)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(BucketList.id))

    def __init__(self, bucketlist_id, name, done=False):
        """ Initialize model with id,name,done defaulting to False """
        self.name = name
        self.done = done
        self.bucketlist_id = bucketlist_id

    def update(self, **kwargs):
        """ Updates the object instance of the model """
        self.name = kwargs.get('name')
        self.done = kwargs.get('done', False)
        db.session.commit()
