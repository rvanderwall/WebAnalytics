__author__ = 'rlv'

import datetime
import re
from LogFileHelper import get_browser_from_agent, get_os_from_agent, get_verb_from_request, get_date_from_string_log_time, get_url_details


class LogRecord:
    REQUESTING_URL = "RequestingUrl"
    DATETIME_OF_REQUEST = "TimeOfRequest"
    TIME_OF_REQUEST = "TimeOnlyOfRequest"

    INDEXABLE_FIELDS = [REQUESTING_URL, DATETIME_OF_REQUEST, TIME_OF_REQUEST]

    all_data_valid = False

    virtual_url = ""
    requesting_url = ""
    RemoteLogName = "-"
    user = ""
    time_of_request = datetime.datetime.utcnow()
    DayOfWeek = 0   # 0 = Monday
    time_only = datetime.time()
    request = ""
    type = ""
    type2 = ""
    section = ""
    name = ""
    verb = "GET"
    status = 200
    bytes = -1
    referrer = ""
    user_agent = ""
    os = ""
    browser = ""
    mozilla_parms = ""
    unique_id = ""
    memory_use = -1
    processing_time = 0
    index = 0

    def __init__(self, str_line):
        data = self.parse_apache_data_line(str_line)
        if data is not None:
            self.set_values_from_data(data)
            self.all_data_valid = True

    def set_values_from_data(self, data):
        self.index = 0
        self.virtual_url = data[self.get_cur_index()]
        self.requesting_url = data[self.get_cur_index()]
        #self.RemoteLogName = data[self.getCurIndex()] # always '-'
        self.user = data[self.get_cur_index()]
        #self.TimeOfRequest = get_date_from_string(data[self.get_cur_index()], "-0400")
        self.time_of_request = get_date_from_string_log_time(data[self.get_cur_index()])
        time_of_req = self.time_of_request.time()
        self.time_only = time_of_req.second + 60 * (time_of_req.minute + 60 * time_of_req.hour)
        self.request = data[self.get_cur_index()]

        url_details = get_url_details(self.request)

        self.type = url_details.type
        self.type2 = url_details.type2
        self.section = url_details.section
        self.name = url_details.name
        self.verb = get_verb_from_request(self.request)
        self.status = int(data[self.get_cur_index()])

        b = data[self.get_cur_index()]
        if b != '-':
            self.bytes = int(b)
        self.referrer = data[self.get_cur_index()]
        self.user_agent = data[self.get_cur_index()]
        self.os = get_os_from_agent(self.user_agent)
        self.browser = get_browser_from_agent(self.user_agent)
        self.mozilla_parms = data[self.get_cur_index()]
        self.unique_id = data[self.get_cur_index()]
        m = data[self.get_cur_index()]
        if m != '-':
            self.memory_use = int(m)
        self.processing_time = int(self.get_cur_index())

    def to_json(self):
        doc = {
            "URL": self.virtual_url,
            self.REQUESTING_URL: self.requesting_url,
            "RemoteLogName": self.RemoteLogName,
            "RemoteUser": self.user,
            self.DATETIME_OF_REQUEST: self.time_of_request,
            "DayOfWeek": self.DayOfWeek,
            self.TIME_OF_REQUEST: self.time_only,
            "Request": self.request,
            "Type": self.type,
            "Type2": self.type2,
            "Section": self.section,
            "Name": self.name,
            "Verb": self.verb,
            "Status": self.status,
            "Bytes": self.bytes,
            "Referrer": self.referrer,
            "UserAgent": self.user_agent,
            "OS": self.os,
            "Browser": self.browser,
            "MozillaParameters": self.mozilla_parms,
            "UniqueId": self.unique_id,
            "MemoryUse": self.memory_use,
            "ProcessingTime": self.processing_time
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

