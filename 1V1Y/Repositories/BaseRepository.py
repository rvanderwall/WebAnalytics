__author__ = 'robert'

import pymongo

class BaseRepository():

    def __init__(self, collection_name, db_host):
        self.client = pymongo.MongoClient(db_host)
        self.db = self.client.LogRecords
        self.collection = self.db[collection_name]

    def drop_collection(self):
        self.collection.drop()

    def insert_record(self, log_record):
        self.collection.save(log_record.to_json())

