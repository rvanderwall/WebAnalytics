__author__ = 'rlv'

import sys
from LogRecordRepository import LogRecordRepository
from ImportLogDataToDB import import_log_data_to_repo, import_cdn_data_to_repo

from SimpleStats import get_simple_stats
import LogRecord

print "PASS"

USE_SMALL_DATA = True

if USE_SMALL_DATA:
    APACHE_LOG = "C:/Users/rlv/Desktop/escweek_sorted.log"
    COLLECTION_NAME = "Digital_Alloy_Small"
    CDN_LOG = "C:/Users/rlv/Desktop/cdnweek_sorted.log"
    CDN_LOG = "C:/Users/rlv/Desktop/cdn_small.txt"
    CDN_COLLECTION_NAME = "Digital_Alloy_CDN_Small"
    USE_ROWS = 1000000
    SKIP_ROWS = 1
    # SKIP_ROWS = sys.maxint
else:
    APACHE_LOG = "C:/Users/rlv/Desktop/escweek_sorted.log"
    COLLECTION_NAME = "Digital_Alloy"
    CDN_LOG = "C:/Users/rlv/Desktop/cdnweek_sorted.log"
    CDN_COLLECTION_NAME = "Digital_Alloy_CDN"
    USE_ROWS = sys.maxint
    #SKIP_ROWS = sys.maxint  # Skip all, do only verification.
    SKIP_ROWS = 20  # Only insert every 1 in 20 rows


repo = LogRecordRepository(COLLECTION_NAME)
#import_log_data_to_repo(repo, APACHE_LOG, SKIP_ROWS, USE_ROWS)
get_simple_stats(repo.collection)

repo = LogRecordRepository(CDN_COLLECTION_NAME)
#import_cdn_data_to_repo(repo, CDN_LOG, SKIP_ROWS, USE_ROWS)
get_simple_stats(repo.collection)
