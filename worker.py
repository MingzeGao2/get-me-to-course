import os
import sys
import unittest
import coverage
import datetime
import threading
from threading import Thread

from project import app, db
from project.models import User, Job
import datetime
from multiprocessing import Process
import time 
from  service import sendEmail, getCourse
from pyquery import PyQuery as pq
import mechanize
import cookielib

#service frequency
check_interval = 60

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
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Chrome')]

    jobs = Job.query.all()
    print "----------------------------------"
    for i in xrange(len(jobs)):
        crn = jobs[i].crn
        res = getCourse(br,crn)
        if res:
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), jobs[i].master.email ,res["description"],"avaliable:",jobs[i].available
            jobs[i].timestamp=datetime.datetime.now()
            x = res["remaining"]
            if (x[0] > 0 and x[1] > 0):
                if (not jobs[i].available):
                    jobs[i].available=True
                    jobs[i].timestamp=datetime.datetime.now()
                    db.session.add(jobs[i])
                    db.session.commit()
                if (jobs[i].send_indicator):
                    print ": seats available"
                else:
                    print ": seats available"
                    print "\tSending email to %s"%jobs[i].master.email
                    p = Process(target=sendEmail, args=(res["description"], 0, jobs[i].master.email))
                    p.start()
                    p.join()
                    jobs[i].send_indicator=True
                    db.session.add(jobs[i])
                    db.session.commit()
            # course is not available
            else:
                if (jobs[i].available):
                    jobs[i].timestamp=datetime.datetime.now()
                    jobs[i].available = False
                    db.session.add(jobs[i])
                    db.session.commit()
                if (jobs[i].send_indicator):
                    print ": seats unavailable"
                    # don't send email when seat is not avaliable 
                    # print "\tSending email %s" %jobs[i].master.email                    
                    # p = Process(target=sendEmail, args=(res["description"],1, jobs[i].master.email))
                    # p.start()
                    # p.join()
                    jobs[i].send_indicator=False
                    db.session.add(jobs[i])
                    db.session.commit()
            db.session.add(jobs[i])
            db.session.commit()


while(True):
    thread_count = threading.active_count()
    if thread_count < 2:
        print("create new process")
        Thread(target=worker, args=()).start()
        time.sleep(check_interval)
        
