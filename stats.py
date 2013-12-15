__author__ = 'rlv'

import datetime
import numpy as np
import re

import matplotlib.pyplot as plt
from LogRecordRepository import LogRecordRepository


def stats(logCollection):
    dateString = '2013-09-21T08:00:00Z'
    d1 = datetime.datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%SZ")
    resp = logCollection.aggregate([{"$match" : {"TimeOfRequest" : { "$lt" : d1}}},
                                    {"$project" : {"RequestingUrl" : 1}},
                                    {"$group": {"_id": "$RequestingUrl", "count": {"$sum": 1}}}])
        # resp = logCollection.aggregate([{"$project": {"RequestingUrl": 1}},
        #                                 {"$group": {"_id": "$RequestingUrl"}}])["result"]
    print len(resp["result"])
    for r in resp["result"]:
        requestingURL = r["_id"]
        show_users_for_URL(logCollection, requestingURL)

# Show requests for URL, only for Sept 21.
#requestingURL = "199.195.144.74"
def show_request_for_URL(logCollection, requestingURL):
    dateString = '2013-09-22T00:00:00Z'
    d1 = datetime.datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%SZ")
    resp = logCollection.find({"RequestingUrl": requestingURL, "TimeOfRequest" : { "$lt" : d1}},
                        { "_id" : 0, "TimeOfRequest":1, "Request":1}).sort([("TimeOfRequest", 1)])
    names = {}
    for r in resp:
        print r

# Get users for URL, only for Sept 21.
def show_users_for_URL(logCollection, requestingURL):
    dateString = '2013-09-22T00:00:00Z'
    d1 = datetime.datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%SZ")
    resp = logCollection.find({"RequestingUrl": requestingURL, "TimeOfRequest" : { "$lt" : d1}}, 
                        { "_id" : 0, "Request":1})
    names = {}
    for r in resp:
        userName = extractUserName(r["Request"])
        if userName in names:
            names[userName] += 1
        else:
            names[userName] = 1

    # Only print URLs with more than one name since None will show up in all of them
    if len(names) > 1:
        print requestingURL
        print names


# Pull user name from request of this form:
# "/rss/videos/podcast/1.xml?username=thisisthechris&xid=92a1bef8aa9861d8e66eba"
def extractUserName(request):
    params = request.split('?')
    if len(params) < 2:
        return None
    userParam = params[1].split('&')[0]
    fieldValue = userParam.split('=')
    if fieldValue[0] == "username":
        return fieldValue[1]
    else:
        return None

print "Starting"

COLLECTION_NAME = "DA_WebLog"
repo = LogRecordRepository(COLLECTION_NAME)
stats(repo.collection)

print "Done"