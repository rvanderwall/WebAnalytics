__author__ = 'rlv'

import datetime
import re
from LogFileHelper import get_browser_from_agent, get_os_from_agent, get_verb_from_request, get_date_from_string_cdn_time
import FieldNames as fn


class CDNRecord:

    INDEXABLE_FIELDS = [fn.REQUESTING_URL, fn.DATETIME_OF_REQUEST, fn.TIME_OF_REQUEST]

    all_data_valid = False

    Virtual_URL = ""
    requesting_url = ""
    RemoteLogName = "-"
    user = ""
    time_of_request = datetime.datetime.utcnow()
    day_of_week = 0   # 0 = Monday
    time_only = datetime.time()
    request = ""
    verb = ""
    status = 0
    bytes = -1
    referrer = ""
    user_agent = ""
    os = ""
    browser = ""

    def __init__(self, str_line):
        data = self.parse_cdn_data_line(str_line)
        if data is not None:
            self.set_values_from_data(data)
            self.all_data_valid = True

    def set_values_from_data(self, raw_data):
        self.index = 0
        #self.Virtual_URL = data[self.get_cur_index()]
        self.requesting_url = raw_data[fn.REQUESTING_URL]
        #self.RemoteLogName = data[self.getCurIndex()] # always '-'
        self.user = raw_data[fn.REMOTE_USER]

        self.time_of_request = get_date_from_string_cdn_time(raw_data[fn.DATETIME_OF_REQUEST])
        self.day_of_week = self.time_of_request.weekday()
        time_of_req = self.time_of_request.time()
        self.time_only = time_of_req.second + 60 * (time_of_req.minute + 60 * time_of_req.hour)

        self.request = raw_data[fn.REQUEST]
        self.verb = get_verb_from_request(self.request)
        self.status = int(raw_data[fn.HTTP_STATUS])

        b = raw_data[fn.BYTES_SENT]
        if b != '-':
            self.bytes = int(b)

        self.referrer = raw_data[fn.REFERRER]
        self.user_agent = raw_data[fn.USER_AGENT]
        self.os = get_os_from_agent(self.user_agent)
        self.browser = get_browser_from_agent(self.user_agent)

    def to_json(self):
        doc = {
            fn.URL: self.Virtual_URL,
            fn.REQUESTING_URL: self.requesting_url,
            fn.REMOTE_LOG_NAME: self.RemoteLogName,
            fn.REMOTE_USER: self.user,
            fn.DATETIME_OF_REQUEST: self.time_of_request,
            fn.DAY_OF_WEEK: self.day_of_week,
            fn.TIME_OF_REQUEST: self.time_only,
            fn.REQUEST: self.request,
            fn.HTTP_VERB: self.verb,
            fn.HTTP_STATUS: self.status,
            fn.BYTES_SENT: self.bytes,
            fn.REFERRER: self.referrer,
            fn.USER_AGENT: self.user_agent,
            fn.USER_OS: self.os,
            fn.USER_BROWSER: self.browser
        }
        return doc

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
        if matches is None:
            return None

        groups = matches.groups()
        raw_data = {}
        raw_data[fn.REQUESTING_URL] = groups[0]
        raw_data[fn.REMOTE_USER] = groups[1]
        raw_data[fn.DATETIME_OF_REQUEST] = groups[2]
        raw_data[fn.REQUEST] = groups[3]
        raw_data[fn.HTTP_STATUS] = groups[4]
        raw_data[fn.BYTES_SENT] = groups[5]
        raw_data[fn.REFERRER] = groups[6]
        raw_data[fn.USER_AGENT] = groups[7]
        return raw_data
