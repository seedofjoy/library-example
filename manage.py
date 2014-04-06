# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from flask_library import app, fixtures
from flask_library.models import db


manager = Manager(app)


@manager.command
def create_db():
    "Creates database tables"
    db.create_all()


@manager.command
def drop_all():
    "Drops all tables"
    db.drop_all()
 

@manager.command
def load_fixtures():
    "Installs test data fixtures into the database"
    fixtures.install(app, *fixtures.all_data)


@manager.command
def runserver():
    "Runs the local server"
    app.run()


if __name__ == "__main__":
    manager.run()
