__author__ = 'rlv'

import datetime
import re
from LogFileHelper import get_browser_from_agent, get_os_from_agent, get_verb_from_request, get_date_from_string_cdn_time


class CDNRecord:
    REQUESTING_URL = "RequestingUrl"
    DATETIME_OF_REQUEST = "TimeOfRequest"
    TIME_OF_REQUEST = "TimeOnlyOfRequest"

    INDEXABLE_FIELDS = [REQUESTING_URL, DATETIME_OF_REQUEST, TIME_OF_REQUEST]

    all_data_valid = False

    Virtual_URL = ""
    requesting_url = ""
    RemoteLogName = "-"
    user = ""
    time_of_request = datetime.datetime.utcnow()
    day_of_week = 0   # 0 = Monday
    time_only = datetime.time()
    request = ""
    verb = "GET"
    status = 200
    bytes = -1
    referrer = ""
    user_agent = ""
    os = ""
    browser = ""
    index = 0

    def __init__(self, str_line):
        data = self.parse_cdn_data_line(str_line)
        if data is not None:
            self.set_values_from_data(data)
            self.all_data_valid = True

    def set_values_from_data(self, data):
        self.index = 0
        #self.Virtual_URL = data[self.get_cur_index()]
        self.requesting_url = data[self.get_cur_index()]
        #self.RemoteLogName = data[self.getCurIndex()] # always '-'
        self.user = data[self.get_cur_index()]
        #self.TimeOfRequest = get_date_from_string(data[self.get_cur_index()], "+0000")
        self.time_of_request = get_date_from_string_cdn_time(data[self.get_cur_index()])
        self.day_of_week = self.time_of_request.weekday()
        time_of_req = self.time_of_request.time()
        self.time_only = time_of_req.second + 60 * (time_of_req.minute + 60 * time_of_req.hour)
        self.request = data[self.get_cur_index()]
        self.verb = get_verb_from_request(self.request)
        self.status = int(data[self.get_cur_index()])

        b = data[self.get_cur_index()]
        if b != '-':
            self.bytes = int(b)
        self.referrer = data[self.get_cur_index()]
        self.user_agent = data[self.get_cur_index()]
        self.os = get_os_from_agent(self.user_agent)
        self.browser = get_browser_from_agent(self.user_agent)

    def to_json(self):
        doc = {
            "URL": self.Virtual_URL,
            self.REQUESTING_URL: self.requesting_url,
            "RemoteLogName": self.RemoteLogName,
            "RemoteUser": self.user,
            self.DATETIME_OF_REQUEST: self.time_of_request,
            "DayOfWeek": self.day_of_week,
            self.TIME_OF_REQUEST: self.time_only,
            "Request": self.request,
            "Verb": self.verb,
            "Status": self.status,
            "Bytes": self.bytes,
            "Referrer": self.referrer,
            "UserAgent": self.user_agent,
            "OS": self.os,
            "Browser": self.browser
        }
        return doc

    def get_cur_index(self):
        ii = self.index
        self.index += 1
        return ii

    @staticmethod
    def parse_cdn_data_line(line):
        """
        121.72.190.31 - - [21/Sep/2013:00:00:00 +0000] "GET /themis.download.akamai.com/media/global/images/castfire/mini/25dbe2dc35a286ea0b0d839b7618b929.jpg HTTP/1.1" 200 8910 "http://www.escapistmagazine.com/videos/view/zero-punctuation" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36" "-"

        Regex will match this log format:
        LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" {mod_php_memory_usage}n"

        %h = host - requesting url
        %l = not sure, but it is always '-', remote log name ???
        %u = remote user
        %t = time, in braces
        %r = request, including verb
        %>s = status code
        %b = bytes returned, or '-' on error
        %{Referer}i = referring url
        %{User-Agent}i = browser
        %{memory use}n = bytes used, or '-'
        """

        regex = '(\S*) - (.*) \[(.*)\] "(.*)" (\d*) (\S*) "(.*?)" "(.*?)" "-"'
        matches = re.match(regex, line)
        if matches is not None:
            return matches.groups()
        else:
            return None
