from DigitalAlloy.Repositories.BaseRepository import BaseRepository

__author__ = 'meted'

import collections

from DigitalAlloy.LogFileHelper import get_title_and_description
from DigitalAlloy.Records.VideoInfoRecord import VideoInfoRecord


class VideoRecordRepository(BaseRepository):
    def __init__(self, collection_name):
        BaseRepository.__init__(self, collection_name)

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
