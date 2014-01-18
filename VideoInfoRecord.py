__author__ = 'meted'

import FieldNames as fn

class VideoInfoRecord:
    INDEXABLE_FIELDS = [fn.PUB_DATE]

    xml_index = 0
    channel = ""
    channel_description = ""

    title = ""
    link = ""
    description = ""
    pubdate = ""
    creator = ""
    category = ""

    def __init__(self):
        return

    def to_json(self):
        doc = {
            fn.CHANNEL_INDEX: self.xml_index,
            fn.CHANNEL_TITLE: self.channel,
            fn.CHANNEL_DESCRIPTION: self.channel_description,
            fn.VIDEO_TITLE: self.title,
            fn.VIDEO_LINK: self.link,
            fn.VIDEO_DESCRIPTION: self.description,
            fn.PUB_DATE: self.pubdate,
            fn.VIDEO_CREATOR: self.creator,
            fn.VIDEO_CATEGORY: self.category
        }
        return doc