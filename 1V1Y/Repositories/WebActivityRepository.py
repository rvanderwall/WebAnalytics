__author__ = 'rlv'

from BaseRepository import BaseRepository
from A1Y1V.Records.WebActivityRecord import WebActivityRecord


class WebActivityRecordRepository(BaseRepository):
    def __init__(self, collection_name, db_host):
        BaseRepository.__init__(self, collection_name, db_host)

    def ensure_indexes(self):
        for field in WebActivityRecord.INDEXABLE_FIELDS:
            self.collection.create_index(field)
