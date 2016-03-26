# manage.py
import os
import sys
import unittest
import coverage
import datetime

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from project import app, db
from project.models import User, Job
import datetime
from multiprocessing import Process
import time 
from  service import sendEmail, getCourse
from pyquery import PyQuery as pq
import mechanize
import cookielib

# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(os.environ['APP_SETTINGS'])
#app.config.from_object("project.config.ProductionConfig")

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True, include='project/*')
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    cov.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    cov.erase()

@manager.command
def show_user():
    print "show all users"
    users = User.query.all()
    for user in users:
        print user.email, user.confirmed
@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(
        email="ad@min.com",
        password="admin",
        admin=True,
        confirmed=True,
        confirmed_on=datetime.datetime.now()))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
