# manage.py


import os
import unittest
import coverage

from flask.ext.script import Manager, Server
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
import datetime

# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object("project.config.DevelopmentConfig")

migrate = Migrate(app, db)
manager = Manager(app)
server = Server(host="0.0.0.0", port=5000)
manager.add_command('runserver', server)
# migrations
manager.add_command('db', MigrateCommand)
# service frequency
waittime=60   



def worker():
    # Browser
    br = mechanize.Browser()
    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Chrome')]

    while (True):
        jobs = Job.query.all()
        print "----------------------------------"
        for i in xrange(len(jobs)):
            crn = jobs[i].crn
            res = getCourse(br,crn)
            jobs[i].timestamp=datetime.datetime.now()
            db.session.add(jobs[i])
            db.session.commit()
            if res:
                print jobs[i].master.email ,res["description"],
                x = res["remaining"]
                if (x[0] > 0 and x[1] > 0):
                    if (jobs[i].available):
                        print ": seats available"
                    else:
                        print ": seats available"
                        print "\tSending email to %s"%jobs[i].master.email
                        p = Process(target=sendEmail, args=(res["description"], 0, jobs[i].master.email))
                        p.start()
                        jobs[i].available=True
                        db.session.add(jobs[i])
                        db.session.commit()
                else:
                    if (jobs[i].available):
                        print ": on seats available"
                        print "\tSending email %s" %jobs[i].master.email                    
                        p = Process(target=sendEmail, args=(res["description"],1, jobs[i].master.email))
                        jobs[i].available=False
                        db.session.add(jobs[i])
                        db.session.commit()
                    else:
                        print ": no seats available"
        time.sleep(waittime)

    


def master():
    p = Process(target=worker)
    p.start()



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
    master()
    manager.run()

