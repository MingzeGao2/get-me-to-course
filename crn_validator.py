from pyquery import PyQuery as pq
import mechanize
import cookielib
import time
import smtplib
from multiprocessing import Process
import os
import sys

# sys.stdout = open("validator_log.txt", 'w')
# sys.stderr = open("validator_error.txt", 'w')

base_url = "https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in=120161&crn_in="


def initBrowser():
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
    return br


def is_valid_crn(browser,crn):
    try:
        response = browser.open(base_url+str(crn))

        cls = pq(response.read())("table.datadisplaytable tr")
        result = {}
        result["description"] = pq(cls[0]).text()
    except:
        # return None
        return False
    try:
        result["capacity"]=[int(pq(pq(cls[3])("td")[0]).text()),int(pq(pq(cls[5])("td")[0]).text())]
        result["actual"]=[int(pq(pq(cls[3])("td")[1]).text()),int(pq(pq(cls[5])("td")[1]).text())]
        result["remaining"]=[int(pq(pq(cls[3])("td")[2]).text()),int(pq(pq(cls[5])("td")[2]).text())]
    except:
        result["capacity"]=[int(pq(pq(cls[3])("td")[0]).text()),1]
        result["actual"]=[int(pq(pq(cls[3])("td")[1]).text()),1]
        result["remaining"]=[int(pq(pq(cls[3])("td")[2]).text()),1]
    # return result
    return True


