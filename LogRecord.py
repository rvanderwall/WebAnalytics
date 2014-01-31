__author__ = 'rlv'

import datetime
import re
from bson import ObjectId

from LogFileHelper import get_browser_from_agent, get_os_from_agent, get_verb_from_request, get_date_from_string_log_time, get_url_details
import FieldNames as fn


class LogRecord:
    INDEXABLE_FIELDS = [fn.REQUESTING_URL, fn.DATETIME_OF_REQUEST, fn.TIME_OF_REQUEST, fn.DATA_TYPE, fn.DATA_SUBTYPE]

    all_data_valid = False

    id = None
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
    fixed_name = ""
    description = ""
    username = ""
    verb = ""
    status = 0
    bytes = -1
    referrer = ""
    user_agent = ""
    os = ""
    browser = ""
    mozilla_parms = ""
    unique_id = ""
    memory_use = -1
    processing_time = 0

    def __init__(self, str_line=None):
        if str_line is not None:
            data = self.parse_apache_data_line(str_line)
            if data is not None:
                self.set_values_from_data(data)
                self.all_data_valid = True
            else:
                self.all_data_valid = False


    def set_values_from_data(self, raw_data):
        self.id = ObjectId()
        self.virtual_url = raw_data[fn.URL]
        self.requesting_url = raw_data[fn.REQUESTING_URL]
        #self.RemoteLogName = data[self.getCurIndex()] # always '-'
        self.user = raw_data[fn.REMOTE_USER]

        self.time_of_request = get_date_from_string_log_time(raw_data[fn.DATETIME_OF_REQUEST])
        self.day_of_week = self.time_of_request.weekday()
        time_of_req = self.time_of_request.time()
        self.time_only = time_of_req.second + 60 * (time_of_req.minute + 60 * time_of_req.hour)

        self.request = raw_data[fn.REQUEST]
        self.verb = get_verb_from_request(self.request)
        self.status = int(raw_data[fn.HTTP_STATUS])

        url_details = get_url_details(self.request)
        self.type = url_details.type
        self.type2 = url_details.type2
        self.section = url_details.section
        self.name = url_details.name
        self.username = ""

        b = raw_data[fn.BYTES_SENT]
        if b != '-':
            try:
                self.bytes = int(b)
            except:
                print "BAD BYTES FIELD"
                print b
                self.bytes = 0

        self.referrer = raw_data[fn.REFERRER]
        self.user_agent = raw_data[fn.USER_AGENT]
        self.os = get_os_from_agent(self.user_agent)
        self.browser = get_browser_from_agent(self.user_agent)

        self.mozilla_parms = raw_data[fn.MOZILLA_PARAMS]
        self.unique_id = raw_data[fn.UNIQUE_ID]

        m = raw_data[fn.MEMORY_USE]
        if m != '-':
            try:
                self.memory_use = int(m)
            except:
                print "BAD MEMORY FIELD"
                print m
                self.memory_use = 0
        try:
            p = raw_data[fn.PROCESSING_TIME]
            self.processing_time = int(p)
        except:
            print "BAD PROCESSOR TIME FIELD"
            print
            self.processing_time = 0

    def to_json(self):
        doc = {
            fn.DATA_ID: self.id,
            fn.URL: self.virtual_url,
            fn.REQUESTING_URL: self.requesting_url,
            fn.REMOTE_LOG_NAME: self.RemoteLogName,
            fn.REMOTE_USER: self.user,
            fn.DATETIME_OF_REQUEST: self.time_of_request,
            fn.DAY_OF_WEEK: self.DayOfWeek,
            fn.TIME_OF_REQUEST: self.time_only,
            fn.REQUEST: self.request,
            fn.DATA_TYPE: self.type,
            fn.DATA_SUBTYPE: self.type2,
            fn.DATA_SECTION: self.section,
            fn.DATA_NAME: self.name,
            fn.DATA_FIXED_NAME: self.fixed_name,
            fn.DATA_DESCRIPTION: self.description,
            fn.DATA_USERNAME: self.username,
            fn.HTTP_VERB: self.verb,
            fn.HTTP_STATUS: self.status,
            fn.BYTES_SENT: self.bytes,
            fn.REFERRER: self.referrer,
            fn.USER_AGENT: self.user_agent,
            fn.USER_OS: self.os,
            fn.USER_BROWSER: self.browser,
            fn.MOZILLA_PARAMS: self.mozilla_parms,
            fn.UNIQUE_ID: self.unique_id,
            fn.MEMORY_USE: self.memory_use,
            fn.PROCESSING_TIME: self.processing_time
        }
        return doc

    def from_json(self, json):
        self.id = json[fn.DATA_ID]
        self.virtual_url = json[fn.URL]
        self.requesting_url = json[fn.REQUESTING_URL]
        self.RemoteLogName = json[fn.REMOTE_LOG_NAME]
        self.user = json[fn.REMOTE_USER]
        self.time_of_request = json[fn.DATETIME_OF_REQUEST]
        self.DayOfWeek = json[fn.DAY_OF_WEEK]
        self.time_only = json[fn.TIME_OF_REQUEST]
        self.request = json[fn.REQUEST]
        self.type = json[fn.DATA_TYPE]
        self.type2 = json[fn.DATA_SUBTYPE]
        self.section = json[fn.DATA_SECTION]
        self.name = json[fn.DATA_NAME]
        self.fixed_name = json[fn.DATA_FIXED_NAME]
        self.description = json[fn.DATA_DESCRIPTION]
        self.username = json[fn.DATA_USERNAME]
        self.verb = json[fn.HTTP_VERB]
        self.status = json[fn.HTTP_STATUS]
        self.bytes = json[fn.BYTES_SENT]
        self.referrer = json[fn.REFERRER]
        self.user_agent = json[fn.USER_AGENT]
        self.os = json[fn.USER_OS]
        self.browser = json[fn.USER_BROWSER]
        self.mozilla_parms = json[fn.MOZILLA_PARAMS]
        self.unique_id = json[fn.UNIQUE_ID]
        self.memory_use = json[fn.MEMORY_USE]
        self.processing_time = json[fn.PROCESSING_TIME]


    @staticmethod
    def try_regex1(line):
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
        if matches is None:
            return None

        groups = matches.groups()
        if groups[10].find('"') != -1:
            return None

        return groups

    @staticmethod
    def parse_apache_data_line(line):
        groups = LogRecord.try_regex1(line)
        if groups is None:
            return None

        raw_data = {}
        raw_data[fn.URL] = groups[0]
        raw_data[fn.REQUESTING_URL] = groups[1]
        raw_data[fn.REMOTE_USER] = groups[2]
        raw_data[fn.DATETIME_OF_REQUEST] = groups[3]
        raw_data[fn.REQUEST] = groups[4]
        raw_data[fn.HTTP_STATUS] = groups[5]
        raw_data[fn.BYTES_SENT] = groups[6]
        raw_data[fn.REFERRER] = groups[7]
        raw_data[fn.USER_AGENT] = groups[8]
        raw_data[fn.MOZILLA_PARAMS] = groups[9]
        raw_data[fn.UNIQUE_ID] = groups[10]
        raw_data[fn.MEMORY_USE] = groups[11]
        raw_data[fn.PROCESSING_TIME] = groups[12]
        return raw_data


def test0():
    logLine = 'URL REQ_URL - Rem User [21/Sep/2013:06:32:01 -0400] "GET REQ" 200 227176 "REF" "USR AGENT" "MOZ" Uj1 414 1'
    data = LogRecord.parse_apache_data_line(logLine)
    assert data[fn.URL] == "URL"
    assert data[fn.REQUESTING_URL] == "REQ_URL"
    assert data[fn.REMOTE_USER] == "Rem User"
    assert data[fn.DATETIME_OF_REQUEST] == "21/Sep/2013:06:32:01 -0400"
    assert data[fn.REQUEST] == "GET REQ"
    assert data[fn.HTTP_STATUS] == "200"
    assert data[fn.BYTES_SENT] == "227176"
    assert data[fn.REFERRER] == "REF"
    assert data[fn.USER_AGENT] == "USR AGENT"
    assert data[fn.MOZILLA_PARAMS] == "MOZ"
    assert data[fn.UNIQUE_ID] == "Uj1"
    assert data[fn.MEMORY_USE] == "414"
    assert data[fn.PROCESSING_TIME] == "1"
    print "PASS0"


def test1():
    logLine = 'www.escapistmagazine.com 80.149.31.40 - Eagle Est1986 [24/Sep/2013:10:56:14 -0400] "GET /rss/videos/podcast/101-7908c74999845d359b932967635cd965.xml?uid=226565 HTTP/1.1" 200 227176 "-" "iTunes/11.1 (Macintosh; OS X 10.7.5) AppleWebKit/534.57.7" "- -" UkGoDgoAAGgAAFCvorsAAABM 2621440 1'
    data = LogRecord.parse_apache_data_line(logLine)
    assert data[fn.URL] == "www.escapistmagazine.com"
    assert data[fn.REQUESTING_URL] == "80.149.31.40"
    assert data[fn.REMOTE_USER] == "Eagle Est1986"
    assert data[fn.DATETIME_OF_REQUEST] == "24/Sep/2013:10:56:14 -0400"
    assert data[fn.REQUEST] == "GET /rss/videos/podcast/101-7908c74999845d359b932967635cd965.xml?uid=226565 HTTP/1.1"
    assert data[fn.HTTP_STATUS] == "200"
    assert data[fn.BYTES_SENT] == "227176"
    assert data[fn.REFERRER] == "-"
    assert data[fn.USER_AGENT] == "iTunes/11.1 (Macintosh; OS X 10.7.5) AppleWebKit/534.57.7"
    assert data[fn.MOZILLA_PARAMS] == "- -"
    assert data[fn.UNIQUE_ID] == "UkGoDgoAAGgAAFCvorsAAABM"
    assert data[fn.MEMORY_USE] == "2621440"
    assert data[fn.PROCESSING_TIME] == "1"
    print "PASS1"


if __name__ == "__main__":
    test0()
    test1()
