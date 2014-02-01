__author__ = 'MeteD'

from datetime import datetime
import pymongo
import config


TEST_COLLECTION = "TestData"


def populate_test_data():
    doc1 = {
        "url": "cnn.com",
        "date": datetime.utcnow(),
        "username": "mete"
    }

    doc2 = {
        "url": "news.bbc.com",
        "date": datetime.utcnow(),
        "username": "robert"
    }

    doc3 = {
        "url": "abc.com",
        "date": datetime.utcnow(),
        "username": ""
    }

    doc4 = {
        "url": "nbc.com",
        "date": datetime.utcnow(),
        "username": "joe"
    }

    doc5 = {
        "url": "cbs.com",
        "date": datetime.utcnow(),
        "username": ""
    }

    test_repository = TestRepository(TEST_COLLECTION)
    test_repository.drop_collection()
    test_repository.save_record(doc1)
    test_repository.save_record(doc2)
    test_repository.save_record(doc3)
    test_repository.save_record(doc4)
    test_repository.save_record(doc5)


def get_data():
    test_repository = TestRepository(TEST_COLLECTION)
    return test_repository.get_records()


def clear_username():
    test_repository = TestRepository(TEST_COLLECTION)
    test_repository.clear_username()


class TestRepository():
    def __init__(self, collection_name):
        self.client = pymongo.MongoClient(config.host)
        self.db = self.client.TestRecords
        self.collection = self.db[collection_name]

    def drop_collection(self):
        self.collection.drop()

    def save_record(self, log_record):
        self.collection.save(log_record)

    def get_records(self):
        return self.collection.find()

    def clear_username(self):
        self.db.eval('db.TestData.update({},{$set:{username:\'\'}}, false, true)')


populate_test_data()
# clear_username()

docs = get_data()

for doc in docs:
    print doc

pass