import config

__author__ = 'meted'

import pymongo
import VideoInfoRecord


class VideoRecordRepository:
    def __init__(self, collection_name):
        self.client = pymongo.MongoClient(config.host)
        self.db = self.client.LogRecords
        self.collection = self.db[collection_name]
        #self.ensure_indexes()

    def drop_collection(self):
        self.collection.drop()

    def insert_record(self, video_info_record):
        self.collection.insert(video_info_record.to_json())

    def ensure_indexes(self):
        for field in VideoInfoRecord.VideoInfoRecord.INDEXABLE_FIELDS:
            self.collection.create_index(field)