__author__ = 'rlv'

import BaseRepository
import Records.WebActivityRecord as WebActivityRecord


class WebActivityRecordRepository(BaseRepository):
    def __init__(self, collection_name):
        BaseRepository.__init__(self, collection_name)

    def ensure_indexes(self):
        for field in WebActivityRecord.INDEXABLE_FIELDS:
            self.collection.create_index(field)
