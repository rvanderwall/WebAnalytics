__author__ = 'robert'

from BaseRepository import BaseRepository
from DigitalAlloy.Records.CDNRecord import CDNRecord

class CDNRecordRepository(BaseRepository):
    def __init__(self, collection_name):
        BaseRepository.__init__(self, collection_name)

    def ensure_indexes(self):
        for field in CDNRecord.CDNRecord.INDEXABLE_FIELDS:
            self.collection.create_index(field)
