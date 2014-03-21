__author__ = 'robert'

import Repositories.WebActivityRepository as warr
import Records.FieldNames as fn
import StatPkg.Plots as p

from config import db_host, COLLECTION_WEBLOG

def simple_stats(logCollection):
    resp = logCollection.count()
    print "NumberOfRecords: %d" % (resp)

    resp = logCollection.aggregate([{"$project": {fn.USER_IP: 1}},
                                    {"$group": {"_id": "$" + fn.USER_IP}},
                                    {"$group": {"_id": 1, "count": { "$sum" : 1}}}])
    print "Unique requestor IP addresses:"
    print resp["result"]

    resp = logCollection.aggregate([{"$project": {fn.REFERRER: 1}},
                                        {"$group": {"_id": "$" + fn.REFERRER}},
                                        {"$group": {"_id": 1, "count": { "$sum" : 1}}}])
    print "Unique referrers:"
    print resp["result"]


if __name__ == "__main__":
    print("Run Stats")
    repo = warr.WebActivityRecordRepository(COLLECTION_WEBLOG, db_host)
    #simple_stats(repo.collection)
    p.plot_data_over_TOD(repo.collection)