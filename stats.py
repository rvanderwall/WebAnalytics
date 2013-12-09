__author__ = 'rlv'

import datetime
import numpy as np
import re

import matplotlib.pyplot as plt
from LogRecordRepository import LogRecordRepository


def stats(logCollection):
    requestingURL = "199.195.144.74"
    dateString = '2013-09-22T00:00:00Z'
    d1 = datetime.datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%SZ")
    resp = logCollection.find({"RequestingUrl": requestingURL, "TimeOfRequest" : { "$lt" : d1}}, 
                        { "_id" : 0, "TimeOfRequest":1, "Request":1}).sort([("TimeOfRequest", 1)])
    for r in resp:
        print r


print "Starting"

COLLECTION_NAME = "DA_WebLog"
repo = LogRecordRepository(COLLECTION_NAME)
stats(repo.collection)
