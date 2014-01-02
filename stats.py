__author__ = 'rlv'

import datetime
import FieldNames as fn
from SimpleStats import get_simple_stats
from Repositories import LogRecordRepository as lr

dateString = '2013-09-21T08:00:00Z'
dateString = '2013-09-22T00:00:00Z'
d1 = datetime.datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%SZ")


# Get list of unique URLs for dates before d1, then show the users for those URLs
def user_stats(logCollection):
    resp = logCollection.aggregate([{"$match" : {fn.DATETIME_OF_REQUEST : { "$lt" : d1}}},
                                    {"$project" : {fn.REQUESTING_URL : 1}},
                                    {"$group": {"_id": "$" + fn.REQUESTING_URL, "count": {"$sum": 1}}}])
    print "Unique requesting IPs for dates before " + str(d1)
    print len(resp["result"])
    for r in resp["result"]:
        requestingURL = r["_id"]
        show_users_for_URL(logCollection, requestingURL, d1)


def show_request_for_URL(logCollection, requestingURL):
    resp = logCollection.find({fn.REQUESTING_URL: requestingURL, fn.DATETIME_OF_REQUEST : { "$lt" : d1}},
                        { "_id" : 0, fn.DATETIME_OF_REQUEST:1, fn.REQUEST:1}).sort([(fn.DATETIME_OF_REQUEST, 1)])
    names = {}
    for r in resp:
        print r


# Get users for URL
def show_users_for_URL(logCollection, requestingURL, maxDate):
    resp = logCollection.find({fn.REQUESTING_URL: requestingURL, fn.DATETIME_OF_REQUEST : { "$lt" : maxDate}},
                        { "_id" : 0, fn.REQUEST:1})
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

repo = lr.LogRecordRepository(fn.COLLECTION_WEBLOG)
get_simple_stats(repo.collection)
#user_stats(repo.collection)

print "Done"

