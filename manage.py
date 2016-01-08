#!/usr/bin/env python
from flask.ext.script import Manager
from bucket.app import create_app
from bucket.models import db, User

manager = Manager(create_app)


@manager.command
def createdb(testdata=False):
    """Initializes the database """
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        if testdata:
            user = User(username='adelle', password='hello')
            db.session.add(user)
            db.session.commit()

if __name__ == '__main__':
    manager.run()
