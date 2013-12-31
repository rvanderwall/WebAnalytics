__author__ = 'meted'

import FieldNames as fn

class VideoInfoRecord:
    INDEXABLE_FIELDS = [fn.PUB_DATE]

    channel = ""
    title = ""
    link = ""
    description = ""
    pubdate = ""

    def __init__(self):
        return

    def to_json(self):
        doc = {
            fn.VIDEO_CHANNEL: self.channel,
            fn.VIDEO_TITLE: self.title,
            fn.VIDEO_LINK: self.link,
            fn.VIDEO_DESCRIPTION: self.description,
            fn.PUB_DATE: self.pubdate
        }
        return doc