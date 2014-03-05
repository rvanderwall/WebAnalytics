__author__ = 'rlv'

from BaseRepository import BaseRepository
import A1Y1V.Records.WebActivityRecord as war


class WebActivityRecordRepository(BaseRepository):
    def __init__(self, collection_name, db_host):
        BaseRepository.__init__(self, collection_name, db_host)

    def ensure_indexes(self):
        for field in war.INDEXABLE_FIELDS:
            self.collection.create_index(field)
