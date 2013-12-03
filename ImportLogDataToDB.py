__author__ = 'rlv'

import sys
from LogRecord import LogRecord
from CDNRecord import CDNRecord


def import_log_data_to_repo(repo, log_file, skip_rows=1, max_rows=sys.maxint):
    f = open(log_file, 'r')
    lineNum = 0
    repo.dropCollection()
    for line in f:
        lineNum += 1
        logRecord = LogRecord(line)
        if logRecord.all_data_valid:
            if lineNum % 100000 == 0:
                print "PROCESSING LINE {0}".format(lineNum)
            if lineNum % skip_rows == 0:
                try:
                    repo.insertRecord(logRecord)
                except Exception:
                    print "ERROR INSERTING LINE {0}".format(lineNum)
                    print line
        else:
            print "ERROR in line {0}".format(lineNum)
        if lineNum > max_rows:
            break
    print "PROCESSED {0} LINES".format(lineNum)


def import_cdn_data_to_repo(repo, log_file, skip_rows=1, max_rows=sys.maxint):
    f = open(log_file, 'r')
    lineNum = 0
    repo.dropCollection()
    for line in f:
        lineNum += 1
        cdnRecord = CDNRecord(line)
        if cdnRecord.All_Data_Valid:
            if lineNum % 100000 == 0:
                print "PROCESSING LINE {0}".format(lineNum)
            if lineNum % skip_rows == 0:
                try:
                    repo.insertRecord(cdnRecord)
                except Exception:
                    print "ERROR INSERTING LINE {0}".format(lineNum)
                    print line
        else:
            print "ERROR PARSING LINE {0}".format(lineNum)
        if lineNum > max_rows:
            break
    print "PROCESSED {0} LINES".format(lineNum)
