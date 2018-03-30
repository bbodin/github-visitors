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


import requests
import json
import pprint


print ""
print "*********************************"
print "** GitHub data retrieving tool **"
print "*********************************"
print ""



'''
Arguments parsing
'''

parser = argparse.ArgumentParser(description='Retrieve and store github traffic logs.')
parser.add_argument('--repository', type=str, required=True, help="github repository (ie. pamela-project/slambench)")
parser.add_argument('--token', type=str, help="Not recommanded, if not set, it will be asked." )
parser.add_argument('--archive', type=str, help="file where to load and save data.")
parser.add_argument('--plot', action='store_true', help="A plot will be generate if set.")
args = parser.parse_args()

repository = args.repository
archive    = args.archive
plot       = args.plot

if args.token == None :
    token   = getpass.getpass('Please type your token: ')
else :
    token   = args.token



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


for key in data.keys() :
    if not isinstance(key, int): 
        print "INVALID DATA"
        exit(1)

        
'''
Main process
'''

    
r = requests.get('https://api.github.com/repos/%s/traffic/views?access_token=%s' % (repository,token))
if(r.ok):
    repoItem = json.loads(r.text or r.content)

    for f in repoItem["views"] :
        timestamp = datetime.datetime.strptime(f["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        timestamp = int(time.mktime(timestamp.timetuple()) + timestamp.microsecond / 1e6)
        
        unique = int(f["uniques"])
        total = int(f["count"])
        if not timestamp in data :
            data[timestamp] = {'unique_visitor': 0, 'total_visitor': 0,
                               'unique_clone': 0, 'total_clone': 0}
        data[timestamp]["unique_visitor"] = unique
        data[timestamp]["total_visitor"] = total
        
else :
    print ("Error")
    exit (1)

   
r = requests.get('https://api.github.com/repos/%s/traffic/clones?access_token=%s' % (repository,token))
if(r.ok):
    repoItem = json.loads(r.text or r.content)
    for f in repoItem["clones"] :
        timestamp = datetime.datetime.strptime(f["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        timestamp = int(time.mktime(timestamp.timetuple()) + timestamp.microsecond / 1e6)
        unique = int(f["uniques"])
        total = int(f["count"])
        if not timestamp in data :
            data[timestamp] = {'unique_visitor': 0, 'total_visitor': 0,
                               'unique_clone': 0, 'total_clone': 0}
        data[timestamp]["unique_clone"] = unique
        data[timestamp]["total_clone"] = total
        
else :
    print ("Error")
    exit (1)

    

    
r = requests.get('https://api.github.com/repos/%s/traffic/popular/referrers?access_token=%s' % (repository,token))
if(r.ok):
    repoItem = json.loads(r.text or r.content)
    for f in repoItem :
        print f["count"] , f["referrer"]
else :
    print ("Error")


    
    
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
