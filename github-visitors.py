#!/usr/bin/python

import urllib2
import urllib
import re
import cookielib,Cookie
import getpass
import ast
import time
import datetime
import argparse
import matplotlib.pyplot as plt

'''
Initialisation
'''

cookies = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
urllib2.install_opener(opener)



def generate_github_token() :

    url="https://github.com/login"
    request = urllib2.Request(url)
    sock=urllib2.urlopen(request)
    content=sock.read()
    sock.close()
    try :
        token = re.search("input name=\"authenticity_token\" type=\"hidden\" value=\"([^\"]+)\"",content).group(1)
        return token
    except :
        return None

    

def open_github_session(token,username,password) :

    fields = {
        'commit' : "Signin",
        'authenticity_token' : token,
        'login' : username,
        'password' : password,
    }
    request = urllib2.Request("https://github.com/session", urllib.urlencode(fields).encode().replace("Signin","Sign%20in"))
    sock=urllib2.urlopen(request)
    content2=sock.read()
    sock.close()

    return True

def retrieve_github_data(repository,data) :


    request = urllib2.Request("https://github.com/" + repository + "/graphs/clone-activity-data")
    request.add_header("x-requested-with", "XMLHttpRequest")
    sock=urllib2.urlopen(request)
    clones_data=sock.read()
    sock.close()

    request = urllib2.Request("https://github.com/" + repository + "/graphs/traffic-data")
    request.add_header("x-requested-with", "XMLHttpRequest")
    sock=urllib2.urlopen(request)
    traffic_data=sock.read()
    sock.close()
    
    clones_data = ast.literal_eval(clones_data)
    traffic_data = ast.literal_eval(traffic_data)
    
    for elem in traffic_data["counts"] :
        data[int(elem["bucket"])] = {}
        data[int(elem["bucket"])]["unique_visitor"] = int(elem["unique"])
        data[int(elem["bucket"])]["total_visitor"] = int(elem["total"])
    for elem in clones_data["counts"] :
        data[int(elem["bucket"])]["unique_clone"] = int(elem["unique"])
        data[int(elem["bucket"])]["total_clone"] = int(elem["total"])

    return isinstance(clones_data, dict) and  isinstance(traffic_data, dict) 



print ""
print "*********************************"
print "** GitHub data retrieving tool **"
print "*********************************"
print ""



'''
Arguments parsing
'''

parser = argparse.ArgumentParser(description='Retrieve and store github traffic logs.')
parser.add_argument('--username', type=str, required=True, help="github username")
parser.add_argument('--repository', type=str, required=True, help="github repository (ie. pamela-project/slambench)")
parser.add_argument('--password', type=str, help="Not recommanded, if not set, it will be asked." )
parser.add_argument('--archive', type=str, help="file where to load and save data.")
parser.add_argument('--plot', action='store_true', help="A plot will be generate if set.")
args = parser.parse_args()

username   = args.username
repository = args.repository
archive    = args.archive
plot       = args.plot

if args.password == None :
    password   = getpass.getpass('Please type your password for %s: ' % username)
else :
    password   = args.password



print ""
print "Initialisation..."

'''
Load previous data
'''

data = {}

if archive :
    try :
        ark =  open(archive, 'rw+')
        previous = ark.read()
        data = ast.literal_eval(previous)
        print "Load archive file '%s'." %archive
        print "Contained %d elements" % len(data.keys())
    except :
        print "Read-only operation failed on the archive file '%s'." %archive

if not isinstance(data, dict):
    print "Archive Error"
    exit(1)
    

'''
Main process
'''
    
print ""
print "Generate Token..."

token = generate_github_token()

if token != None :
    print "Token OK"
else :
    print "Token Error"
    exit(1)


    
print ""
print "Open session..."

session = open_github_session(token,username,password)
    
if session :
    print "Session OK"
else :
    print "Session Error"
    exit(1)


    
print ""
print "Retrieve data..."
retrieve = retrieve_github_data(repository,data)

if retrieve :
    print "Data OK"
    print "Data is %d elements" % len(data.keys())
else :
    print "Data Error"
    exit(1)



'''
Plot or print
'''
if plot :

    x   = [datetime.datetime.fromtimestamp(elem) for elem in sorted(data.keys())]
    y_1 = [elem["unique_visitor"] for elem in data.values()]
    y_2 = [elem["unique_clone"] for elem in data.values()]
    
    plt.plot(x,y_1, label = "unique_visitor")
    plt.plot(x,y_2, label = "unique_clone")
    plt.gcf().autofmt_xdate()

    plt.show()

else :
    print ""
    print ""
    print data
    print ""

    
if archive :
    print ""
    print "Save data."
    ark =  open(archive, 'w')
    data_str = str(data)
    ark.write(data_str)
    ark.close()
    print "Saved."
    
print ""
