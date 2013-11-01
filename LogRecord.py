__author__ = 'rlv'

import datetime
import re
from LogFileHelper import get_date_from_string, get_browser_from_agent, get_OS_from_agent, get_verb_from_request

class LogRecord:

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
    Mozilla_parms = ""
    UniqueId = ""
    memoryUse = -1
    ProcessingTime = 0
    index = 0

    def __init__(self, str_line):
        data = self.parse_apache_data_line(str_line)
        if data != None:
            self.set_values_from_data(data)
            self.All_Data_Valid = True

    def set_values_from_data(self, data):
        self.index = 0
        self.Virtual_URL = data[self.get_cur_index()]
        self.Requesting_URL = data[self.get_cur_index()]
        #self.RemoteLogName = data[self.getCurIndex()] # always '-'
        self.User = data[self.get_cur_index()]
        self.TimeOfRequest = get_date_from_string(data[self.get_cur_index()], "-0400")
        self.DayOfWeek = self.TimeOfRequest.weekday()
        time_of_req = self.TimeOfRequest.time()
        self.TimeOnly = time_of_req.second + 60 *(time_of_req.minute + 60*time_of_req.hour)
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
        self.Mozilla_parms = data[self.get_cur_index()]
        self.UniqueId = data[self.get_cur_index()]
        m = data[self.get_cur_index()]
        if m != '-':
            self.memoryUse = int(m)
        self.ProcessingTime = int(self.get_cur_index())

    def toJSON(self):
        doc = {
            "URL" : self.Virtual_URL,
            self.REQUESTING_URL : self.Requesting_URL,
            "RemoteLogName" : self.RemoteLogName,
            "RemoteUser" : self.User,
            self.DATETIME_OF_REQUEST : self.TimeOfRequest,
            "DayOfWeek" : self.DayOfWeek,
            self.TIME_OF_REQUEST : self.TimeOnly,
            "Request" : self.Request,
            "Verb" : self.Verb,
            "Status" : self.Status,
            "Bytes" : self.Bytes,
            "Referrer" : self.Referrer,
            "UserAgent" : self.UserAgent,
            "OS" : self.OS,
            "Browser" : self.Browser,
            "MozillaParameters" : self.Mozilla_parms,
            "UniqueId" : self.UniqueId,
            "MemoryUse" : self.memoryUse,
            "ProcessingTime" : self.ProcessingTime
        }
        return doc

    def get_cur_index(self):
        ii = self.index
        self.index += 1
        return ii


    def parse_apache_data_line(self, line):
        """
            Regex will match this log format:
             LogFormat "%V %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"
                      \"%{X-Moz}i %{X-Purpose}i\" %{UNIQUE_ID}e %{mod_php_memory_usage}n %T"
            %V = virtual
            %h = host
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
        if matches != None:
            return matches.groups()
        else:
            return None

