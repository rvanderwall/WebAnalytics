__author__ = 'robert'

import collections

from DigitalAlloy.Repositories.BaseRepository import BaseRepository

FN_ID = "id"
FN_DATE = "date"
FN_DAY_OF_WEEK = "day_of_week"
FN_TIME_OF_DAY = "time_only"
FN_WORD_COUNT = "words"
FN_PAGE_COUNT = "pages"
FN_THREAD_ID = "threadID"
FN_POST_ID = "postID"
FN_TYPE = "type"
FN_CONTENT_ID = "contentID"
FN_TAGS = "tags"

class NewsInfoRepository(BaseRepository):
    def __init__(self, collection_name):
        BaseRepository.__init__(self, collection_name)

    def ensure_indexes(self):
        self.collection.create_index(FN_DATE)

