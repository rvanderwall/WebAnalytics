__author__ = 'rlv'

import sys
from LogRecordRepository import LogRecordRepository
from VideoRecordRepository import VideoRecordRepository
from ImportLogDataToDB import import_log_data_to_repo, import_video_information_to_repo

from SimpleStats import get_simple_stats

print "PASS"

IMPORT_VIDEO_INFORMATION = False
CREATE_WEBLOG_WITH_ONLY_VIDEO_REQUESTS = True

MODE_VERIFY_ONLY = 0
MODE_SPARSE = 1
MODE_FULL = 2
MODE_TEST = 3

MODE = MODE_TEST
# DATA_PATH = "M:\MorningBeacon\DigitalAlloyData"
DATA_PATH = "/media/analytics/workspace/projects/digitalalloy/data"
APACHE_LOG = DATA_PATH + "/escweek_sorted.log"
CDN_LOG = DATA_PATH + "/cdnweek_sorted.log"

if MODE == MODE_VERIFY_ONLY:
    COLLECTION_NAME = "DA_WebLog_Sparce"
    CDN_COLLECTION_NAME = "DA_CDNLog_Sparce"
    USE_ROWS = sys.maxint
    SKIP_ROWS = sys.maxint
elif MODE == MODE_SPARSE:
    COLLECTION_NAME = "DA_WebLog_Sparce"
    CDN_COLLECTION_NAME = "DA_CDNLog_Sparce"
    USE_ROWS = 24000000
    SKIP_ROWS = 20  # Only insert every 1 in 20 rows
elif MODE == MODE_FULL:
    COLLECTION_NAME = "DA_WebLog"
    CDN_COLLECTION_NAME = "DA_CDNLog"
    USE_ROWS = sys.maxint
    SKIP_ROWS = 1  # Don't actually Skip any
elif MODE == MODE_TEST:
    COLLECTION_NAME = "DA_WebLog_Test"
    CDN_COLLECTION_NAME = "DA_CDNLog_Test"
    USE_ROWS = sys.maxint
    SKIP_ROWS = sys.maxint
else:
    print "Invalid mode"

# repo = LogRecordRepository(COLLECTION_NAME)
# import_log_data_to_repo(repo, APACHE_LOG, SKIP_ROWS, USE_ROWS)
# repo.ensure_indexes()
# get_simple_stats(repo.collection)

#repo = LogRecordRepository(CDN_COLLECTION_NAME)
#import_cdn_data_to_repo(repo, CDN_LOG, SKIP_ROWS, USE_ROWS)
#repo.ensure_indexes()
#get_simple_stats(repo.collection)

if IMPORT_VIDEO_INFORMATION:
    COLLECTION_NAME = "DA_Video_Info"
    repo = VideoRecordRepository(COLLECTION_NAME)
    import_video_information_to_repo(repo)
    repo.ensure_indexes()

if CREATE_WEBLOG_WITH_ONLY_VIDEO_REQUESTS:
    VIDEO_INFO_COLLECTION_NAME = "DA_Video_Info"
    VIDEO_WEB_LOG_COLLECTION_NAME = "DA_WebLog_Videos"
    USE_ROWS = sys.maxint
    SKIP_ROWS = 1  # Don't actually Skip any

    video_info_repo = VideoRecordRepository(VIDEO_INFO_COLLECTION_NAME)
    descriptions = video_info_repo.get_descriptions()

    web_log_repo = LogRecordRepository(VIDEO_WEB_LOG_COLLECTION_NAME)
    import_log_data_to_repo(web_log_repo, APACHE_LOG, SKIP_ROWS, USE_ROWS, only_videos=True,
                            descriptions=descriptions)
    # web_log_repo.ensure_indexes()


