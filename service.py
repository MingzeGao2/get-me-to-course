"""
easy_install pip
pip install pyquery
pip install mechanize

Mechanize is used, so that it is easy to later add automatic registration.
The login function logs you in to enterprise. All that is now necessary is
the actual automatic registration code...
"""
from pyquery import PyQuery as pq
import mechanize
import cookielib
import time
import smtplib
from multiprocessing import Process
import os

#A list of the CRNs of each class
# courses = [36091, 36047, 43357,58792, 30128, 49546, 65086, 46792, 40091,  32108, 32103, 40083]
#40083

# url for query
base_url = "https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in=120158&crn_in="



def get_msg(description, specification):
    if  specification == 0:
        return  "\r\n".join([
            "From: mingze.gao.gmz@gmail.com",
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
    from_addr = "mingze.gao.gmz@gmail.com"
    # to_addr = ["mingzegao1994.gsdfmz@gsdfmail.com", "mingze.gao.gmz@gmailsdf.com"]
    # to_addr= "sdf.sdlfjsldjf"
    username = 'mingze.gao.gmz@gmail.com'
    password = 'qtncejoibqbpgvfs'
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


