from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import sqlalchemy
import hashlib
from exceptions.handler import NullReferenceException

db = SQLAlchemy()
class_mapper = sqlalchemy.orm.class_mapper


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
        json_dict = dict()
        result_list = []
        for property in class_mapper(self.__class__).iterate_properties:
            if property.key == 'user':
                continue
            if property.key == 'items':
                items = getattr(self, property.key)
                # serialize objects to json format
                for item in items:
                    if callable(getattr(item, 'to_json')):
                        result = item.to_json()
                        result_list.append(result)
                json_dict[property.key] = result_list
                continue

            json_dict[property.key] = getattr(self, property.key)

        return json_dict


class User(Base):
    """Maps to users table """
    __tablename__ = 'users'
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    bucketlists = db.relationship(
        'BucketList', order_by='BucketList.id')

    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha512(password).hexdigest()

    def password_is_valid(self, password):
        """Validates user password """
        return self.password == hashlib.sha512(password).hexdigest()


class BucketList(Base):
    """Maps to the bucketlists table """
    __tablename__ = 'bucketlists'
    name = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    user = db.relationship('User')
    items = db.relationship('BucketListItem')

    def __init__(self, created_by, name):
        """ Initialize with the creator and name of bucketlist """
        self.created_by = created_by
        self.name = name

    @staticmethod
    def get_all(user_id):
        """Returns logged in user bucketlist data """
        return BucketList.query.filter_by(created_by=user_id)


class Session(Base):
    """Maps to session table """
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
        """Initializes model with id,name,done defaulting to False """
        self.name = name
        self.done = False if done else False
        self.bucketlist_id = bucketlist_id

    def update(self, **kwargs):
        """Updates the object instance of the model """
        self.name = kwargs.get('name')
        if BucketListItem.query.filter_by(name=self.name).first():
            if kwargs.get('done') == 'True' or kwargs.get('done') == 'true':
                self.done = True
            else:
                self.done = False
            db.session.commit()
        else:
            raise NullReferenceException()
