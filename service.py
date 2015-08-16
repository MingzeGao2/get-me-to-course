from pyquery import PyQuery as pq
import mechanize
import cookielib
import time
import smtplib
from multiprocessing import Process
import os
import sys

sys.stdout = open("log.txt", 'w')
sys.stderr = open("error.txt", 'w')

# url for query
base_url = "https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in=120158&crn_in="



def get_msg(description, specification):
    if  specification == 0:
        return  "\r\n".join([
            "From:master.getmeclasses@gmail.com",
            "To: mingzegao1994.gmz@gmail.com",
            "Subject: Catch This",
            "",
            "SEATS AVAILABLE " + description
        ])
    if specification == 1:
        return "\r\n".join([
            "From: mingze.gao.gmz@gmail.com",
            "To: mingzegao1994.gmz@gmail.com",
            "Subject: NO!!!",
            "",
            "SEATS UNAVAILABLE " + description
        ])

    
def sendEmail(description, specification, to_addr):
    from_addr = "master.getmeclassses@gmail.com"
    # to_addr = ["mingzegao1994.gsdfmz@gsdfmail.com", "mingze.gao.gmz@gmailsdf.com"]
    # to_addr= "sdf.sdlfjsldjf"
    username = 'master.getmeclassses@gmail.com'
    password = 'dtyblbfoozujdsrl'
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username,password)
        msg = get_msg(description, specification)
        server.sendmail(from_addr, to_addr, msg)
        server.quit()
        print "successfully sent the mail"
    except:
        print "failed to send mail"


def getCourse(browser,crn):
    try:
        response = browser.open(base_url+str(crn))

        cls = pq(response.read())("table.datadisplaytable tr")
        result = {}
        result["description"] = pq(cls[0]).text()
    except:
        return None
    try:
        result["capacity"]=[int(pq(pq(cls[3])("td")[0]).text()),int(pq(pq(cls[5])("td")[0]).text())]
        result["actual"]=[int(pq(pq(cls[3])("td")[1]).text()),int(pq(pq(cls[5])("td")[1]).text())]
        result["remaining"]=[int(pq(pq(cls[3])("td")[2]).text()),int(pq(pq(cls[5])("td")[2]).text())]
    except:
        result["capacity"]=[int(pq(pq(cls[3])("td")[0]).text()),1]
        result["actual"]=[int(pq(pq(cls[3])("td")[1]).text()),1]
        result["remaining"]=[int(pq(pq(cls[3])("td")[2]).text()),1]
    return result


