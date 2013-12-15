__author__ = 'meted'


class VideoInfoRecord:
    PUB_DATE = "Pubdate"
    INDEXABLE_FIELDS = [PUB_DATE]

    channel = ""
    title = ""
    link = ""
    description = ""
    pubdate = ""

    def __init__(self):
        return

    def to_json(self):
        doc = {
            "Channel": self.channel,
            "Title": self.title,
            "link": self.link,
            "Description": self.description,
            self.PUB_DATE: self.pubdate
        }
        return doc