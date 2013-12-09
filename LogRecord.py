__author__ = 'rlv'

import datetime
import re
from LogFileHelper import get_browser_from_agent, get_OS_from_agent, get_verb_from_request, get_date_from_string_logtime, get_url_details


class LogRecord:
    REQUESTING_URL = "RequestingUrl"
    DATETIME_OF_REQUEST = "TimeOfRequest"
    TIME_OF_REQUEST = "TimeOnlyOfRequest"

    indexable_fields = [REQUESTING_URL, DATETIME_OF_REQUEST, TIME_OF_REQUEST]

    all_data_valid = False

    Virtual_URL = ""
    Requesting_URL = ""
    RemoteLogName = "-"
    User = ""
    TimeOfRequest = datetime.datetime.utcnow()
    DayOfWeek = 0   # 0 = Monday
    TimeOnly = datetime.time()
    Request = ""
    Type = ""
    Type2 = ""
    Section = ""
    Name = ""
    Verb = "GET"
    Status = 200
    Bytes = -1
    Referrer = ""
    UserAgent = ""
    OS = ""
    Browser = ""
    Mozilla_parms = ""
    UniqueId = ""
    memoryUse = -1
    ProcessingTime = 0
    index = 0

    def __init__(self, str_line):
        data = self.parse_apache_data_line(str_line)
        if data is not None:
            self.set_values_from_data(data)
            self.all_data_valid = True

    def set_values_from_data(self, data):
        self.index = 0
        self.Virtual_URL = data[self.get_cur_index()]
        self.Requesting_URL = data[self.get_cur_index()]
        #self.RemoteLogName = data[self.getCurIndex()] # always '-'
        self.User = data[self.get_cur_index()]
        #self.TimeOfRequest = get_date_from_string(data[self.get_cur_index()], "-0400")
        self.TimeOfRequest = get_date_from_string_logtime(data[self.get_cur_index()])
        time_of_req = self.TimeOfRequest.time()
        self.TimeOnly = time_of_req.second + 60 * (time_of_req.minute + 60 * time_of_req.hour)
        self.Request = data[self.get_cur_index()]

        url_details = get_url_details(self.Request)

        self.type = url_details.type
        self.type2 = url_details.type2
        self.section = url_details.section
        self.name = url_details.name
        self.Verb = get_verb_from_request(self.Request)
        self.Status = int(data[self.get_cur_index()])

        b = data[self.get_cur_index()]
        if b != '-':
            self.Bytes = int(b)
        self.Referrer = data[self.get_cur_index()]
        self.UserAgent = data[self.get_cur_index()]
        self.OS = get_OS_from_agent(self.UserAgent)
        self.Browser = get_browser_from_agent(self.UserAgent)
        self.Mozilla_parms = data[self.get_cur_index()]
        self.UniqueId = data[self.get_cur_index()]
        m = data[self.get_cur_index()]
        if m != '-':
            self.memoryUse = int(m)
        self.ProcessingTime = int(self.get_cur_index())

    def to_json(self):
        doc = {
            "URL": self.Virtual_URL,
            self.REQUESTING_URL: self.Requesting_URL,
            "RemoteLogName": self.RemoteLogName,
            "RemoteUser": self.User,
            self.DATETIME_OF_REQUEST: self.TimeOfRequest,
            "DayOfWeek": self.DayOfWeek,
            self.TIME_OF_REQUEST: self.TimeOnly,
            "Request": self.Request,
            "Type": self.type,
            "Type2": self.type2,
            "Section": self.section,
            "Name": self.name,
            "Verb": self.Verb,
            "Status": self.Status,
            "Bytes": self.Bytes,
            "Referrer": self.Referrer,
            "UserAgent": self.UserAgent,
            "OS": self.OS,
            "Browser": self.Browser,
            "MozillaParameters": self.Mozilla_parms,
            "UniqueId": self.UniqueId,
            "MemoryUse": self.memoryUse,
            "ProcessingTime": self.ProcessingTime
        }
        return doc

    def get_cur_index(self):
        ii = self.index
        self.index += 1
        return ii

    @staticmethod
    def parse_apache_data_line(line):
        """
            www.escapistmagazine.com 80.149.31.40 - Eagle Est1986 [24/Sep/2013:10:56:14 -0400] "GET /rss/videos/podcast/101-7908c74999845d359b932967635cd965.xml?uid=226565 HTTP/1.1" 200 227176 "-" "iTunes/11.1 (Macintosh; OS X 10.7.5) AppleWebKit/534.57.7" "- -" UkGoDgoAAGgAAFCvorsAAABM 2621440 1'

            Regex will match this log format:
            LogFormat "%V %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" \"%{X-Moz}i %{X-Purpose}i\" %{UNIQUE_ID}e %{mod_php_memory_usage}n %T"

            %V = virtual
            %h = host - requesting url
            %l = not sure, but it is always '-'
            %u = user
            %t = time, in braces
            %r = request, including verb
            %>s = status code
            %b = bytes returned, or '-' on error
            %{Referer}i = referring url
            %{User-Agent}i = browser
            %{X-Moz}i %{X-Purpose}i = not sure but it is always '- -'
            %UNIQUE_ID = not sure
            %{memory use}n = bytes used, or '-'
            %T = time in mSec.
        :param line:
        :return:
        """
        regex = '(\S*)\s(\S*) - (.*) \[(.*)\] "(.*)" (\d*) (\S*) "(.*?)" "(.*?)" "(.*?)" (\S*) (\S*) (\d*)'
        matches = re.match(regex, line)
        if matches is not None:
            return matches.groups()
        else:
            return None

