__author__ = 'rlv'

import pymongo
import LogRecord


class LogRecordRepository:
    collection = None
    #host="127.0.0.1"
    host="192.168.1.71"

    def __init__(self, collectionName):
        self.client = pymongo.MongoClient(self.host)
        self.db = self.client.LogRecords
        self.collection = self.db[collectionName]
        #self.ensure_indexes()

    def dropCollection(self):
        self.collection.drop()

    def insertRecord(self, logRecord):
        self.collection.insert(logRecord.to_json())


    def ensure_indexes(self):
        for field in LogRecord.LogRecord.indexable_fields:
            self.collection.create_index(field)


# bson.errors.InvalidStringData: strings in documents must be valid UTF-8: 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B329 [FBAN/FBIOS;FBAV/6.4;FBBV/290891;FBDV/iPhone4,1;FBMD/iPhone;FBSN/iPhone OS;FBSV/6.1.3;FBSS/2; FBCR/OrangeEspa\xf1a;FBID/phone;FBLC/es_ES;FBOP/1]'

