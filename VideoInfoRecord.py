__author__ = 'meted'


class VideoInfoRecord:
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
            "Pubdate": self.pubdate
        }
        return doc