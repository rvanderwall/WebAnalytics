import collections
import re
from LogFileHelper import get_title_and_description
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

    def get_descriptions(self):
        descriptions = {}
        for video_info in self.collection.find():
            title, description = get_title_and_description(video_info)
            descriptions[title] = description

        ordered_descriptions = collections.OrderedDict(sorted(descriptions.items()))
        # for k, v in ordered_descriptions.iteritems(): print k, v
        return ordered_descriptions