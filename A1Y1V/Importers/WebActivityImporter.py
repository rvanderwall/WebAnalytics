__author__ = 'rlv'

import sys
import urllib2
from datetime import datetime

from A1Y1V.Records.WebActivityRecord import WebActivityRecord

def import_log_data_to_repo(repo, log_file, skip_rows=1, max_rows=sys.maxint):
    return general_import_log_data_to_repo(repo, log_file, skip_rows, max_rows, WebActivityRecord)

def general_import_log_data_to_repo(repo, log_file, skip_rows, max_rows, LogRecord):
    f = open(log_file, 'r')
    line_num = 0
    repo.drop_collection()

    for line in f:
        line_num += 1
        log_record = LogRecord(line)
        if log_record.all_data_valid:
            if line_num % 100000 == 0:
                print "PROCESSING LINE {0}".format(line_num)
            if line_num % skip_rows == 0:
                try:
                    repo.insert_record(log_record)
                except Exception:
                    print "ERROR INSERTING LINE {0}".format(line_num)
                    print line
        else:
            print "ERROR in line {0}".format(line_num)
        if line_num > max_rows:
            break
    print "PROCESSED {0} LINES".format(line_num)

