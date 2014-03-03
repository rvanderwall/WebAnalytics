from A1Y1V.Records import FieldNames as fn

__author__ = 'rlv'

import datetime

import bson


class LogRecord:
    INDEXABLE_FIELDS = [fn.USER_ID]

    all_data_valid = False

    id = None
    action_type = ""
    member_id = ""
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
        self.id = bson.ObjectId()
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


