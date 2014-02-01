__author__ = 'rlv'

import datetime
import re

import pytz

from LogRecord import LogRecord

from BaseRepository import BaseRepository
import FieldNames as fn
from LogFileHelper import extractUserNameFromRequest


username_regx = re.compile("username", re.IGNORECASE)


class LogRecordRepository(BaseRepository):
    def __init__(self, collection_name):
        BaseRepository.__init__(self, collection_name)

    def ensure_indexes(self):
        for field in LogRecord.INDEXABLE_FIELDS:
            self.collection.create_index(field)

    def add_user_to_log(self, weblog_repo):
        line_num = 0

        #        for video_log in self.collection.find({fn.REQUESTING_URL : "72.14.199.63"},
        # for video_log in self.collection.find({}, {fn.DATA_NAME: 1, fn.DATETIME_OF_REQUEST: 1, fn.REQUESTING_URL: 1}):
        for video_log in self.collection.find():
            line_num += 1
            if line_num % 100000 == 0:
                print "PROCESSING LINE {0}".format(line_num)
            user = weblog_repo.get_user_at_time(video_log[fn.DATETIME_OF_REQUEST], video_log[fn.REQUESTING_URL])
            if user != None:
                print "{0} viewed {1} at {2}".format(user, video_log[fn.DATA_NAME], video_log[fn.DATETIME_OF_REQUEST])
                video_log[fn.DATA_USERNAME] = user
                log_record = LogRecord()
                log_record.from_json(video_log)
                self.insert_record(log_record)
                # self.insert_dictionary(ObjectId(video_log[fn.DATA_ID]), video_log)

    def get_user_at_time(self, time, IP):
        log_timezone = pytz.utc
        d1 = log_timezone.localize(time)
        d2 = d1 - datetime.timedelta(minutes=5)

        res = self.collection.find({fn.DATETIME_OF_REQUEST: {"$lte": d1, "$gt": d2},
                                    fn.REQUEST: username_regx,
                                    fn.REQUESTING_URL: IP}).sort(fn.DATETIME_OF_REQUEST, -1)
        if res.count() > 0:
            req = res[0][fn.REQUEST]
            return extractUserNameFromRequest(req)
        else:
            return None

    def reset_all_usernames(self):
        self.db.eval('db.TestData.update({},{$set:{Username:\'\'}}, false, true)')

