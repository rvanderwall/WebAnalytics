__author__ = 'rlv'

import datetime
import pytz
import re

import LogRecord
from BaseRepository import BaseRepository
import FieldNames as fn
from LogFileHelper import extractUserNameFromRequest

class LogRecordRepository(BaseRepository):
    def __init__(self, collection_name):
        BaseRepository.__init__(self, collection_name)

    def ensure_indexes(self):
        for field in LogRecord.LogRecord.INDEXABLE_FIELDS:
            self.collection.create_index(field)

    def get_user_at_time(self, time, IP):
        log_timezone = pytz.utc
        d1 = log_timezone.localize(time)
        d2 = d1 - datetime.timedelta(minutes=1)
        regx = re.compile("username", re.IGNORECASE)
        res = self.collection.find({fn.DATETIME_OF_REQUEST : {"$lte" : d1, "$gt" : d2},
                                    fn.REQUEST : regx,
                                    fn.REQUESTING_URL : IP}).sort(fn.DATETIME_OF_REQUEST, -1)
        if res.count() > 0:
            req = res[0][fn.REQUEST]
            return extractUserNameFromRequest(req)
        else:
            return None

    def add_user_to_log(self, weblog_repo):
#        for video_log in self.collection.find({fn.REQUESTING_URL : "72.14.199.63"},
        for video_log in self.collection.find({},
                                              { fn.DATA_NAME:1,  fn.DATETIME_OF_REQUEST:1, fn.REQUESTING_URL:1}):
            user = weblog_repo.get_user_at_time(video_log[fn.DATETIME_OF_REQUEST], video_log[fn.REQUESTING_URL])
            if user != None:
                print "{0} viewed {1} at {2}".format(user, video_log[fn.DATA_NAME], video_log[fn.DATETIME_OF_REQUEST])