__author__ = 'rlv'

import LogRecord
from BaseRepository import BaseRepository

class LogRecordRepository(BaseRepository):
    def __init__(self, collection_name):
        BaseRepository.__init__(self, collection_name)

    def ensure_indexes(self):
        for field in LogRecord.LogRecord.INDEXABLE_FIELDS:
            self.collection.create_index(field)
