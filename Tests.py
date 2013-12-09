__author__ = 'rlv'

import sys
from LogRecordRepository import LogRecordRepository
from ImportLogDataToDB import import_log_data_to_repo, import_cdn_data_to_repo, import_video_information_to_repo

from SimpleStats import get_simple_stats
import LogRecord

print "PASS"

MODE_VERIFY_ONLY = 0
MODE_SPARCE = 1
MODE_FULL = 2
MODE_CAPTURE_VIDEO_INFORMATION_ONLY = 3

MODE = MODE_CAPTURE_VIDEO_INFORMATION_ONLY
# DATAPATH = "M:\MorningBeacon\DigitalAlloyData"
DATAPATH = "/media/analytics/workspace/projects/digitalalloy/data"
APACHE_LOG = DATAPATH + "/escweek_sorted.log"
CDN_LOG = DATAPATH + "/cdnweek_sorted.log"

if MODE == MODE_VERIFY_ONLY:
    COLLECTION_NAME = "DA_WebLog_Sparce"
    CDN_COLLECTION_NAME = "DA_CDNLog_Sparce"
    USE_ROWS = sys.maxint
    SKIP_ROWS = sys.maxint
elif MODE == MODE_SPARCE:
    COLLECTION_NAME = "DA_WebLog_Sparce"
    CDN_COLLECTION_NAME = "DA_CDNLog_Sparce"
    USE_ROWS = 24000000
    SKIP_ROWS = 20  # Only insert every 1 in 20 rows
elif MODE == MODE_FULL:
    COLLECTION_NAME = "DA_WebLog"
    CDN_COLLECTION_NAME = "DA_CDNLog"
    USE_ROWS = sys.maxint
    SKIP_ROWS = 1  # Don't actually Skip any
elif MODE == MODE_CAPTURE_VIDEO_INFORMATION_ONLY:
    COLLECTION_NAME = "DA_Video_Info"
    repo = LogRecordRepository(COLLECTION_NAME)
    import_video_information_to_repo(repo)
    exit()
else:
    print "Invalid mode"

repo = LogRecordRepository(COLLECTION_NAME)
import_log_data_to_repo(repo, APACHE_LOG, SKIP_ROWS, USE_ROWS)
repo.ensure_indexes()
get_simple_stats(repo.collection)

#repo = LogRecordRepository(CDN_COLLECTION_NAME)
#import_cdn_data_to_repo(repo, CDN_LOG, SKIP_ROWS, USE_ROWS)
#repo.ensure_indexes()
#get_simple_stats(repo.collection)

