__author__ = 'rlv'

import sys
from LogRecordRepository import LogRecordRepository
from ImportLogDataToDB import import_log_data_to_repo, import_cdn_data_to_repo

from SimpleStats import get_simple_stats
import LogRecord

print "PASS"

USE_SPARSE_DATA = True
DATAPATH = "/media/analytics/workspace/projects/digitalalloy/data"
APACHE_LOG = DATAPATH + "/escweek_sorted.log"
CDN_LOG = DATAPATH + "/cdnweek_sorted.log"

if USE_SPARSE_DATA:
    COLLECTION_NAME = "DA_WebLog_Sparce"
    CDN_COLLECTION_NAME = "DA_CDNLog_Sparce"
    #USE_ROWS = 100000000
    USE_ROWS = sys.maxint
    SKIP_ROWS = 20  # Only insert every 1 in 20 rows
else:
    COLLECTION_NAME = "DA_WebLog"
    CDN_COLLECTION_NAME = "DA_CDNLog"
    USE_ROWS = sys.maxint
    SKIP_ROWS = sys.maxint  # Skip all, do only verification.

repo = LogRecordRepository(COLLECTION_NAME)
import_log_data_to_repo(repo, APACHE_LOG, SKIP_ROWS, USE_ROWS)
repo.ensure_indexes()
get_simple_stats(repo.collection)

#repo = LogRecordRepository(CDN_COLLECTION_NAME)
#import_cdn_data_to_repo(repo, CDN_LOG, SKIP_ROWS, USE_ROWS)
#repo.ensure_indexes()
#get_simple_stats(repo.collection)
