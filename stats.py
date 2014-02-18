__author__ = 'rlv'

import datetime
from LogFileHelper import extractUserNameFromRequest
from Repositories import LogRecordRepository as lr
from Repositories import VideoRecordRepository as vr
from Records import FieldNames as fn


dateString = '2013-09-21T08:00:00Z'
dateString = '2013-09-22T00:00:00Z'
d1 = datetime.datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%SZ")


# Stats for Lord Bane
def lb_stats(logCollection):
    IPs = ["162.243.4.144",
	"162.243.4.145",
	"162.243.4.146",
	"162.243.4.147",
	"162.243.4.148",
	"162.243.4.149",
	"192.241.251.101"]
    for ip in IPs:
        print ("FROM IP {0}").format(ip)
        show_request_for_URL(logCollection, ip)

# Stats for JEdge
def je_stats(logCollection):
    IPs = ["72.14.199.63",
	"162.243.4.144",
	"162.243.4.145",
	"162.243.4.146",
	"162.243.4.147",
	"162.243.4.148",
	"162.243.4.149",
	"192.241.251.101",
    "198.199.109.13"
    ]
    for ip in IPs:
        print ("FROM IP {0}").format(ip)
        show_request_for_URL(logCollection, ip)



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
    for r in resp:
        request = r['Request']
        print r
#        if "username" in request:
#            if "videos" in request:
#                print r


# Get users for URL
def show_users_for_URL(logCollection, requestingURL, maxDate):
    resp = logCollection.find({fn.REQUESTING_URL: requestingURL, fn.DATETIME_OF_REQUEST : { "$lt" : maxDate}},
                        { "_id" : 0, fn.REQUEST:1})
    names = {}
    for r in resp:
        userName = extractUserNameFromRequest(r["Request"])
        if userName in names:
            names[userName] += 1
        else:
            names[userName] = 1

    # Only print URLs with more than one name since None will show up in all of them
    if len(names) > 1:
        print requestingURL
        print names



print "Starting"

repo = lr.LogRecordRepository(fn.COLLECTION_WEBLOG)
#get_simple_stats(repo.collection)
#user_stats(repo.collection)
video_repo = vr.VideoRecordRepository(fn.COLLECTION_VIDEO_WEB_LOG)
je_stats(video_repo.collection)

print
ip="72.14.199.63"
print "All Requests for {0}".format(ip)
show_request_for_URL(repo.collection, ip)
print "Done"

"http://video.escapistmagazine.com/links/4f3701051a03cc034ae75ba38cbd18b6/mp4/escapist/escape-to-the-movies/7359d3a5d2418cefd0e387f944c6b8fc.mp4?8df5e36ee1f3629756e58b9231ba96b55a3980e3ef75885f33a38eec3446c5b14f30d26db194d4a1024638ecbd6de00fecb4c25fec9e18&.mp4"
#> d1 = new Date(2013,8,21,12,13,42)
#ISODate("2013-09-21T16:13:42Z")
#d2 = new Date(d1-10000)
#w.find({"TimeOfRequest" : {$lte : d1, $gt : d2}, "Request" : /username/, RequestingUrl : "72.14.199.63"}).sort({TimeOfRequest : -1})[0]
