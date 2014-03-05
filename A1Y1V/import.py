__author__ = 'rlv'

import sys
from os.path import normpath, join

from config import DATA_PATH, DATA_FILE, COLLECTION_WEBLOG, db_host
import Repositories.WebActivityRepository as warr
from Importers.WebActivityImporter import import_log_data_to_repo

print "START"

MODE_SPARSE = 1
MODE_FULL = 2
MODE_TEST = 3

MODE = MODE_FULL
IMPORT_WEBLOG = True

web_log_file = normpath(join(DATA_PATH, DATA_FILE))

if MODE == MODE_SPARSE:
    log_collection = COLLECTION_WEBLOG + "_sparce"
    USE_ROWS = 24000000
    SKIP_ROWS = 20  # Only insert every 1 in 20 rows
elif MODE == MODE_FULL:
    log_collection = COLLECTION_WEBLOG
    USE_ROWS = sys.maxint
    SKIP_ROWS = 1  # Don't actually Skip any
elif MODE == MODE_TEST:
    log_collection = "TEST_WebLog"
    USE_ROWS = sys.maxint
    SKIP_ROWS = sys.maxint
else:
    print "Invalid mode"

# -----WEB LOGS-----
if IMPORT_WEBLOG:
    repo = warr.WebActivityRecordRepository(log_collection, db_host)
    import_log_data_to_repo(repo, web_log_file, SKIP_ROWS, USE_ROWS)
    repo.ensure_indexes()

