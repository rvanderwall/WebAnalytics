__author__ = 'rlv'

import re
from datetime import timedelta, datetime
from pytz import timezone
import pytz
import collections
from urlparse import urlparse


def get_verb_from_request(request):
    regex = '(\S*)\s.*'
    matches = re.match(regex, request)
    if matches:
        return matches.groups()[0]
    else:
        return "NONE"


def get_browser_from_agent(agent):
    if re.search('chrome', agent, re.I):
        return "Chrome"
    if re.search('firefox', agent, re.I):
        return "FireFox"
    if re.search('itunes', agent, re.I):
        return "iTunes"
    if re.search('safari', agent, re.I):
        return "Safari"
    if re.search('msie', agent, re.I):
        return "IE"
    if re.search('opera', agent, re.I):
        return "Opera"
    return agent


def get_OS_from_agent(agent):
    if re.search('macintosh', agent, re.I):
        return "Mac"
    if re.search('windows', agent, re.I):
        return "Windows"
    if re.search('linux', agent, re.I):
        return "Linux"
    if re.search('iphone', agent, re.I):
        return "iPhone"
    if re.search('ipad', agent, re.I):
        return "iPad"
    return agent


def agent_is_a_bot(agent):
    regex = 'bot |get | get|crawl|slurp|fetch|spider|search|engine|valid|check|finder|^(ruby|java)|libwww|livejournal|heritrix|yandex|urllib|setooz|longurl|grabber|wordpress|pipes|kimengi|larbin|binlar|eventmachine|feed\s+parse|webvac|btwebclient|mediapartners|ocelli'
    if re.search(regex, agent, re.I):
        return True
    else:
        return False


def get_date_from_string(dateString, offset):
    #21/Sep/2013:06:32:01 -0400
    #21/Sep/2013:00:00:00 +0000
    date = datetime.datetime.strptime(dateString, "%d/%b/%Y:%H:%M:%S " + offset)
    return date


def get_date_from_string_logtime(dateString):
    fmt = "%d/%b/%Y:%H:%M:%S"
    logtime = datetime.strptime(dateString[:-6], fmt)
    logtimezone = timezone("Etc/GMT+4")
    loc_logtime = logtimezone.localize(logtime)
    utclogtime = loc_logtime.astimezone(pytz.utc)
    return utclogtime


def get_date_from_string_cdntime(dateString):
    fmt = "%d/%b/%Y:%H:%M:%S"
    logtime = datetime.strptime(dateString[:-6], fmt)
    logtimezone = pytz.utc
    utclogtime = logtimezone.localize(logtime)
    return utclogtime


def get_date_from_string_2(dateString, offset):
    try:
        offset = int(dateString[-5:])
    except:
        print "Error"

    fmt = "%d/%b/%Y:%H:%M:%S"
    delta = timedelta(hours=offset / 100)
    logtime = datetime.strptime(dateString[:-6], fmt)
    logtime -= delta
    return logtime


def get_url_details(request):
    UrlDetail = collections.namedtuple('UrlDetail', 'type type2 section name')
    o = urlparse(request)
    path = o.path
    try:
        #regex = re.compile("(?:\w*)\s/(?P<type>\w*)/(?P<type2>\w*)(?:/(?P<section>.*))?/(?P<name>.*$)", re.IGNORECASE)
        regex = re.compile("(?:\w*)\s/(?P<type>\w*)/(?P<type2>\w*)(?:/(?P<section>[^ \s]*))?/(?P<name>[^ \s]*)", re.IGNORECASE)
        r = regex.search(path)
    except:
        print "Couldn't parse '" + request + "'"
        return UrlDetail()

    if r is not None:
        return UrlDetail(r.group("type"), r.group("type2"), r.group("section"), r.group("name"))
    else:
        print "Couldn't parse '" + request + "'"
        return UrlDetail(None, None, None, None)