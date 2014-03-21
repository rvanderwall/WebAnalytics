__author__ = 'robert'

import os
import re
from datetime import datetime
from DigitalAlloy.LogFileHelper import get_datetime_from_string
import Repositories.NewsInfoRepository as nr

COLLECTION_NAME = "DA_NewsInfo"

class NewsInfoRecord:
    data_valid = False
    data = {}

    def __init__(self, line):
        self.data = parse_from_line(line)
        if self.data != None:
            self.data_valid = True

    def to_json(self):
        return self.data

def strip_quotes(field):
    return field[1:-1]

def get_int_part(field):
    return int(strip_quotes(field))

PATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
def parse_from_line(line):
    if line == None:
        return None
    if len(line)< 15:
        return None
    if line[0] == '#':
        return None

    #parts = line.split(",")
    parts = PATTERN.split(line)[1::2]
    parsing = {}
    parsing[nr.FN_ID] = get_int_part(parts[0])
    datetime_of_request = get_datetime_from_string(strip_quotes(parts[1]))
    parsing[nr.FN_DATE] = datetime_of_request
    parsing[nr.FN_DAY_OF_WEEK] = datetime_of_request.weekday()
    time_of_req = datetime_of_request.time()
    parsing[nr.FN_TIME_OF_DAY] = time_of_req.second + 60 * (time_of_req.minute + 60 * time_of_req.hour)

    parsing[nr.FN_WORD_COUNT] = get_int_part(parts[2])
    parsing[nr.FN_THREAD_ID] = get_int_part(parts[3])
    parsing[nr.FN_POST_ID] = get_int_part(parts[4])
    parsing[nr.FN_TYPE] = strip_quotes(parts[5])
    parsing[nr.FN_CONTENT_ID] = get_int_part(parts[6])
    parsing[nr.FN_TAGS] = strip_quotes(parts[7])
    parsing[nr.FN_PAGE_COUNT] = get_int_part(parts[8][:-1]) # skip \n at end
    return parsing

def import_news_from_csv(repo, log_file):
    f = open(log_file, 'r')
    line_num = 0
    repo.drop_collection()

    for line in f:
        line_num += 1
        log_record = NewsInfoRecord(line)
        if log_record.data_valid:
            if line_num % 10000 == 0:
                print "PROCESSING LINE {0}".format(line_num)
            repo.insert_record(log_record)
        else:
            print "ERROR in line {0}".format(line_num)
    print "PROCESSED {0} LINES".format(line_num)



if __name__ == "__main__":
    print("Import News from CSV")
    print("PWD={0}").format(os.getcwd())

    repo = nr.NewsInfoRepository(COLLECTION_NAME)
    import_news_from_csv(repo, "../../data/Escapist/news.csv")
