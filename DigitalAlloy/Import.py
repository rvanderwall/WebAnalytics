__author__ = 'rlv'

import sys
from os.path import normpath, join

from DigitalAlloy.ImportLogDataToDB import import_log_data_to_repo, import_cdn_data_to_repo, import_video_information_to_repo
from DigitalAlloy.config import DATA_PATH, WEB_LOG_DATA, CDN_LOG_DATA
import Records.FieldNames as fn
import Repositories.CDNRecordRepository as cr
import Repositories.VideoRecordRepository as vr
import Repositories.LogRecordRepository as lr


print "START"

MODE_SPARSE = 1
MODE_FULL = 2
MODE_TEST = 3

MODE = MODE_TEST
IMPORT_WEBLOG = False
IMPORT_CDNLOG = False
IMPORT_VIDEO_INFORMATION_ONLY = False
CREATE_WEBLOG_WITH_VIDEO_REQUESTS_ONLY = False
UPDATE_WEBLOG_WITH_USERS = True

APACHE_LOG = normpath(join(DATA_PATH, WEB_LOG_DATA))
CDN_LOG = normpath(join(DATA_PATH, CDN_LOG_DATA))

if MODE == MODE_SPARSE:
    LOG_COLLECTION_NAME = fn.COLLECTION_WEBLOG_SPARCE
    CDN_COLLECTION_NAME = fn.COLLECTION_CDNLOG_SPARCE
    USE_ROWS = 24000000
    SKIP_ROWS = 20  # Only insert every 1 in 20 rows
elif MODE == MODE_FULL:
    LOG_COLLECTION_NAME = fn.COLLECTION_WEBLOG
    CDN_COLLECTION_NAME = fn.COLLECTION_CDNLOG
    USE_ROWS = sys.maxint
    SKIP_ROWS = 1  # Don't actually Skip any
elif MODE == MODE_TEST:
    LOG_COLLECTION_NAME = "TEST_WebLog"
    CDN_COLLECTION_NAME = "TEST_CDNLog"
    USE_ROWS = sys.maxint
    SKIP_ROWS = sys.maxint
else:
    print "Invalid mode"

# -----WEB LOGS-----
if IMPORT_VIDEO_INFORMATION_ONLY:
    repo = vr.VideoRecordRepository(fn.COLLECTION_VIDEO_INFO)
    import_video_information_to_repo(repo)
    repo.ensure_indexes()

if IMPORT_WEBLOG:
    video_info_repo = vr.VideoRecordRepository(fn.COLLECTION_VIDEO_INFO)
    descriptions = video_info_repo.get_descriptions()
    repo = lr.LogRecordRepository(LOG_COLLECTION_NAME)
    import_log_data_to_repo(repo, APACHE_LOG, SKIP_ROWS, USE_ROWS, descriptions=descriptions)
    repo.ensure_indexes()

if CREATE_WEBLOG_WITH_VIDEO_REQUESTS_ONLY:
    USE_ROWS = sys.maxint
    SKIP_ROWS = 1  # Don't actually Skip any

    video_info_repo = vr.VideoRecordRepository(fn.COLLECTION_VIDEO_INFO)
    descriptions = video_info_repo.get_descriptions()

    web_log_repo = lr.LogRecordRepository(fn.COLLECTION_VIDEO_WEB_LOG)
    import_log_data_to_repo(web_log_repo, APACHE_LOG, SKIP_ROWS, USE_ROWS, only_videos=True, descriptions=descriptions)
    web_log_repo.ensure_indexes()

if UPDATE_WEBLOG_WITH_USERS:
    repo = lr.LogRecordRepository(fn.COLLECTION_WEBLOG)
    video_web_log_repo = lr.LogRecordRepository(fn.COLLECTION_VIDEO_WEB_LOG)
    video_web_log_repo.reset_all_usernames()
    video_web_log_repo.add_user_to_log(repo)

# -----CDN LOGS-----
if IMPORT_CDNLOG:
    repo = cr.CDNRecordRepository(CDN_COLLECTION_NAME)
    import_cdn_data_to_repo(repo, CDN_LOG, SKIP_ROWS, USE_ROWS)
    repo.ensure_indexes()

