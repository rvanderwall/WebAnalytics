__author__ = 'robert'

import Repositories.WebActivityRepository as warr
from config import db_host, COLLECTION_WEBLOG
import Records.FieldNames as fn

def simple_stats(logCollection):
    resp = logCollection.count()
    print "NumberOfRecords: %d" % (resp)

    resp = logCollection.aggregate([{"$project": {fn.USER_IP: 1}},
                                    {"$group": {"_id": "$" + fn.USER_IP}},
                                    {"$group": {"_id": 1, "count": { "$sum" : 1}}}])
    print "Unique requestor IP addresses:"
    print resp


if __name__ == "__main__":
    repo = warr.WebActivityRecordRepository(COLLECTION_WEBLOG, db_host)
    simple_stats(repo.collection)
