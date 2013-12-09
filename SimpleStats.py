__author__ = 'rlv'

import datetime
import numpy as np
import re

import matplotlib.pyplot as plt


def get_simple_stats(logCollection):
    resp = logCollection.count()
    print "NumberOfRecords: %d" % (resp)

    other_stats = True
    if other_stats:
        resp = logCollection.aggregate([{"$group": {"_id": "$Verb", "count": {"$sum": 1}}}])
        print "Verbs:"
        print resp["result"]

        # resp = logCollection.aggregate([{"$project": {"RequestingUrl": 1}},
        #                                 {"$group": {"_id": "$RequestingUrl"}}])["result"]
        # print "Unique requestors: %d" % (len(resp))

        resp = logCollection.aggregate([{"$group": {"_id": "$Status", "count": {"$sum": 1}}}])
        print "Status Codes:"
        print resp["result"]

        resp = logCollection.aggregate([{"$group": {"_id": "$Referrer"}}])
        print "All referrers:"
        print len(resp["result"])

        regx = re.compile("escapistmagazine", re.IGNORECASE)
        check = {"Referrer": regx}
        resp = logCollection.aggregate([{"$match": check}, {"$group": {"_id": "$Referrer"}}])
        print "Escapist referrers:"
        print len(resp["result"])

        regx = re.compile("gurl", re.IGNORECASE)
        check = {"Referrer": regx}
        resp = logCollection.aggregate([{"$match": check}, {"$group": {"_id": "$Referrer"}}])
        print "Gurl referrers:"
        print len(resp["result"])

    data = []
    for hour in range(0, 24):
        for minute in range(0, 60):
            start = 60 * (hour * 60 + minute)
            end = start + 60
            #resp = logCollection.find({"TimeOnlyOfRequest": {"$gte": start, "$lt": end}, "Verb": "GET", "Status": 200})
            resp = logCollection.find(
                {"TimeOnlyOfRequest": {"$gte": start, "$lt": end}, "Verb": "GET", "Status": 200}).distinct(
                "RequestingUrl")
            #data.append(resp.count())
            data.append(len(resp))

    #time_axis = np.arange(0, len(data) / 60, 1.0 / 60)
    time_axis = np.arange(0, 24, 1.0 / 60)
    plt.plot(time_axis, data)
    plt.title("Hits Per Minute")
    plt.ylabel("Number of Hits From Unique IPs")
    plt.xlabel("Time - 24hr Format - In GMT-0")
    plt.show()

    cum = 0
    for day in range(20, 30, 1):
        date1String = '2013-09-' + str(day) + 'T00:16:09Z'
        date2String = '2013-09-' + str(day + 1) + 'T00:16:09Z'
        d1 = datetime.datetime.strptime(date1String, "%Y-%m-%dT%H:%M:%SZ")
        d2 = datetime.datetime.strptime(date2String, "%Y-%m-%dT%H:%M:%SZ")
        count = logCollection.find({"TimeOfRequest": {"$gte": d1, "$lt": d2}}).count()
        cum = cum + count
        print "Count for day %d is %d" % (day, count)
    print "days cumulative: %d" % (cum)


# d = db.Digital_Alloy_CDN
# d.find({RequestingUrl : "80.149.31.40"}, {_id : 0, TimeOnlyOfRequest : 1, Request : 1}).pretty()
# a = db.Digital_Alloy
#  a.find({RequestingUrl : "80.149.31.40"},{_id:0, RemoteUser:1,Request:1,TimeOnlyOfRequest:1,OS:1}).pretty()

