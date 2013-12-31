__author__ = 'robert'

import config
import pymongo


class BaseRepository():
    def __init__(self, collection_name):
        self.client = pymongo.MongoClient(config.host)
        self.db = self.client.LogRecords
        self.collection = self.db[collection_name]

    def drop_collection(self):
        self.collection.drop()

    def insert_record(self, log_record):
        self.collection.insert(log_record.to_json())

