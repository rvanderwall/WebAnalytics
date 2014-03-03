__author__ = 'rlv'

import datetime
import re
import numpy as np

import matplotlib.pyplot as plt

from DigitalAlloy.Records import FieldNames as fn


def get_simple_stats(logCollection):

    resp = logCollection.count()
    print "NumberOfRecords: %d" % (resp)

    other_stats = True
    if other_stats:
        if False:   #Already recored, don't need to run each time.
            resp = logCollection.aggregate([{"$group": {"_id": "$Verb", "count": {"$sum": 1}}}])
            print "Verbs:"
            print resp["result"]

            resp = logCollection.aggregate([{"$group": {"_id": "$Status", "count": {"$sum": 1}}}])
            print "Status Codes:"
            print resp["result"]

            #  Try with standard aggregate -- I get 'Doc too big' error
            #resp = logCollection.aggregate([{"$project": {fn.REQUESTING_URL: 1}},
            #                                 {"$group": {"_id": "$" + fn.REQUESTING_URL}}])["result"]
            #print "Unique requestors: %d" % (len(resp))

            # Try with distinct -- Still get 'Doc too big'
            #resp = logCollection.distinct(fn.REQUESTING_URL)
            #print "Unique requestors: %d" % resp.count()

            # Try within the pipeline
            resp = logCollection.aggregate([{"$project": {fn.REQUESTING_URL: 1}},
                                            {"$group": {"_id": "$" + fn.REQUESTING_URL}},
                                            {"$group": {"_id": 1, "count": { "$sum" : 1}}}])
            print "Unique requestors:"
            print resp

        resp = logCollection.aggregate([{"$project": {fn.REFERRER: 1}},
                                            {"$group": {"_id": "$" + fn.REFERRER}},
                                            {"$group": {"_id": 1, "count": { "$sum" : 1}}}])
        print "Unique referrers:"
        print resp["result"]

        regx = re.compile("escapistmagazine", re.IGNORECASE)
        check = {"Referrer": regx}
        resp = logCollection.aggregate([{"$match": check},
                                        {"$project": {fn.REFERRER: 1}},
                                        {"$group": {"_id": "$" + fn.REFERRER}},
                                        {"$group": {"_id": 1, "count": { "$sum" : 1}}}])
        print "Escapist referrers:"
        print resp["result"]

        regx = re.compile("gurl", re.IGNORECASE)
        check = {"Referrer": regx}
        resp = logCollection.aggregate([{"$match": check}, {"$group": {"_id": "$" + fn.REFERRER}}])
        print "Gurl referrers:"
        print len(resp["result"])

    data = []
    for hour in range(0, 24):
        for minute in range(0, 60):
            start = 60 * (hour * 60 + minute)
            end = start + 60
            resp = logCollection.find(
                {fn.TIME_OF_REQUEST: {"$gte": start, "$lt": end}, fn.HTTP_VERB: "GET", fn.HTTP_STATUS: 200}).distinct(fn.REQUESTING_URL)
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
        count = logCollection.find({fn.DATETIME_OF_REQUEST: {"$gte": d1, "$lt": d2}}).count()
        cum = cum + count
        print "Count for day %d is %d" % (day, count)
    print "days cumulative: %d" % (cum)


