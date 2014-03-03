__author__ = 'robert'

import pymongo
from A_1Y1V import config


class BaseRepository():
    def __init__(self, collection_name):
        self.client = pymongo.MongoClient(config.host)
        self.db = self.client.LogRecords
        self.collection = self.db[collection_name]

    def drop_collection(self):
        self.collection.drop()

    def insert_record(self, log_record):
        self.collection.save(log_record.to_json())

    # def insert_dictionary(self, id, log_dictionary):
    #     self.collection.save(log_dictionary)

