__author__ = 'rlv'

import datetime
import re
from LogFileHelper import get_browser_from_agent, get_OS_from_agent, get_verb_from_request, get_date_from_string_cdntime


class CDNRecord:
    REQUESTING_URL = "RequestingUrl"
    DATETIME_OF_REQUEST = "TimeOfRequest"
    TIME_OF_REQUEST = "TimeOnlyOfRequest"

    indexable_fields = [REQUESTING_URL, DATETIME_OF_REQUEST, TIME_OF_REQUEST]

    All_Data_Valid = False

    Virtual_URL = ""
    Requesting_URL = ""
    RemoteLogName = "-"
    User = ""
    TimeOfRequest = datetime.datetime.utcnow()
    DayOfWeek = 0   # 0 = Monday
    TimeOnly = datetime.time()
    Request = ""
    Verb = "GET"
    Status = 200
    Bytes = -1
    Referrer = ""
    UserAgent = ""
    OS = ""
    Browser = ""
    index = 0

    def __init__(self, str_line):
        data = self.parse_CDN_data_line(str_line)
        if data != None:
            self.set_values_from_data(data)
            self.All_Data_Valid = True

    def set_values_from_data(self, data):
        self.index = 0
        #self.Virtual_URL = data[self.get_cur_index()]
        self.Requesting_URL = data[self.get_cur_index()]
        #self.RemoteLogName = data[self.getCurIndex()] # always '-'
        self.User = data[self.get_cur_index()]
        #self.TimeOfRequest = get_date_from_string(data[self.get_cur_index()], "+0000")
        self.TimeOfRequest = get_date_from_string_cdntime(data[self.get_cur_index()])
        self.DayOfWeek = self.TimeOfRequest.weekday()
        time_of_req = self.TimeOfRequest.time()
        self.TimeOnly = time_of_req.second + 60 * (time_of_req.minute + 60 * time_of_req.hour)
        self.Request = data[self.get_cur_index()]
        self.Verb = get_verb_from_request(self.Request)
        self.Status = int(data[self.get_cur_index()])

        b = data[self.get_cur_index()]
        if b != '-':
            self.Bytes = int(b)
        self.Referrer = data[self.get_cur_index()]
        self.UserAgent = data[self.get_cur_index()]
        self.OS = get_OS_from_agent(self.UserAgent)
        self.Browser = get_browser_from_agent(self.UserAgent)

    def toJSON(self):
        doc = {
            "URL": self.Virtual_URL,
            self.REQUESTING_URL: self.Requesting_URL,
            "RemoteLogName": self.RemoteLogName,
            "RemoteUser": self.User,
            self.DATETIME_OF_REQUEST: self.TimeOfRequest,
            "DayOfWeek": self.DayOfWeek,
            self.TIME_OF_REQUEST: self.TimeOnly,
            "Request": self.Request,
            "Verb": self.Verb,
            "Status": self.Status,
            "Bytes": self.Bytes,
            "Referrer": self.Referrer,
            "UserAgent": self.UserAgent,
            "OS": self.OS,
            "Browser": self.Browser
        }
        return doc

    def get_cur_index(self):
        ii = self.index
        self.index += 1
        return ii

    def parse_CDN_data_line(self, line):
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
        if matches != None:
            return matches.groups()
        else:
            return None
