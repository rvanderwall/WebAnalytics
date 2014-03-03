__author__ = 'rlv'

import datetime
import bson
import FieldNames as fn

from A1Y1V.Parsers.WebActivityLogParser import parse_line
import A1Y1V.Parsers.WebActivityLogParser as walp
from A1Y1V.Parsers.WebTimeHelper import get_date_from_string_log_time
from A1Y1V.Parsers.WebAgentHelper import get_browser_from_agent, get_os_from_agent

class WebActivityRecord:
    INDEXABLE_FIELDS = [fn.USER_ID, fn.ACTIVITY_DATE]

    all_data_valid = False

    id = None
    transaction_id = 0
    action_type = ""
    member_id = ""
    user = ""

    time_of_request = datetime.datetime.utcnow()
    DayOfWeek = 0   # 0 = Monday
    time_only = datetime.time()

    campaign_id = 0
    trademark_id = 0
    product_type_id = 0
    inventory_id = 0
    category_id = 0
    custom_list_id = 0

    user_ip = ""
    request = ""
    referrer = ""
    user_agent = ""
    os = ""
    browser = ""
    extra_data = ""


    def __init__(self, str_line=None):
        if str_line is not None:
            data = parse_line(str_line)
            if data is not None:
                self.set_values_from_data(data)
                self.all_data_valid = True
            else:
                self.all_data_valid = False


    def set_values_from_data(self, raw_data):
        self.id = bson.ObjectId()
        self.transaction_id = raw_data[walp.ID]
        # TODO:  Look up action
        self.action_type = raw_data[walp.ACTION_TYPE_ID]
        self.member_id = raw_data[walp.MEMBER_ID]
        # TODO: Look up user
        self.user = raw_data[walp.MEMBER_ID]

        self.time_of_request = get_date_from_string_log_time(raw_data[walp.ACTIVITY_DATE])
        self.day_of_week = self.time_of_request.weekday()
        time_of_req = self.time_of_request.time()
        self.time_only = time_of_req.second + 60 * (time_of_req.minute + 60 * time_of_req.hour)

        self.campaign_id = raw_data[walp.CAMPAIGN_ID]
        self.trademark_id = raw_data[walp.TRADEMARK_ID]
        self.product_type_id = raw_data[walp.PRODUCT_TYPE_ID]
        self.inventory_id = raw_data[walp.INVENTORY_ID]
        self.category_id = raw_data[walp.CATEGORY_ID]
        self.custom_list_id = raw_data[walp.CUSTOM_LIST_ID]

        self.user_ip = raw_data[walp.USER_IP]
        self.request = raw_data[walp.REQUESTED_URL]

        self.referrer = raw_data[walp.REFERRER]
        self.user_agent = raw_data[walp.USER_AGENT]
        self.os = get_os_from_agent(self.user_agent)
        self.browser = get_browser_from_agent(self.user_agent)

        self.extra_data = raw_data[walp.EXTRA_DATA]

    def to_json(self):
        doc = {
            fn.ID : self.id,
            fn.TRANSACTION_ID: self.transaction_id,
            fn.ACTION: self.action_type,
            fn.MEMBER_ID: self.member_id,
            fn.USER_ID: self.user,
            fn.ACTIVITY_DATE: self.time_of_request,
            fn.ACTIVITY_DAY: self.day_of_week,
            fn.ACTIVITY_TIME: self.time_only,

            fn.CAMPAIGN_ID: self.campaign_id,
            fn.TRADEMARK_ID: self.trademark_id,
            fn.PRODUCT_TYPE_ID: self.product_type_id,
            fn.INVENTORY_ID: self.inventory_id,
            fn.CATEGORY_ID: self.category_id,
            fn.CUSTOM_LIST_ID: self.custom_list_id,

            fn.USER_IP: self.user_ip,
            fn.REQUESTED_URL: self.request,
            fn.REFERRER: self.referrer,
            fn.USER_AGENT: self.user_agent,
            fn.USER_OS: self.os,
            fn.USER_BROWSER: self.browser,
            fn.EXTRA_DATA: self.extra_data
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


