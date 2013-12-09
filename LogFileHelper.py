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


#regex = re.compile("(?:\w*)\s/(?P<type>\w*)/(?P<type2>\w*)(?:/(?P<section>.*))?/(?P<name>.*$)", re.IGNORECASE)
#regex = re.compile("(?:\w*)\s/(?P<type>\w*)/(?P<type2>\w*)(?:/(?P<section>[^ \s]*))?/(?P<name>[^ \s]*)", re.IGNORECASE)
regex = re.compile("/(?P<type>\w*)/(?P<type2>\w*)(?:/(?P<section>[^ \s]*))?/(?P<name>[^ \s]*)", re.IGNORECASE)


def get_url_details(request):
    UrlDetail = collections.namedtuple('UrlDetail', 'type type2 section name')
    #o = urlparse(request)
    #path = o.path
    matches = re.match('GET (.*) HTTP/1.[01]', request)
    if matches is None:
        return UrlDetail(None, None, None, None)
    request_path = matches.groups()[0]
    path = request_path.split('?')[0]
    parts = path.split('/')

    if len(parts) == 1:   # /
        return UrlDetail(None, None, None, None)
    if len(parts) == 2:   # /t
        return UrlDetail(parts[1], None, None, None)
    if len(parts) == 3:   # /t/u
        return UrlDetail(parts[1], parts[2], None, None)
    if len(parts) == 4:   # /t/u/v
        return UrlDetail(parts[1], parts[2], None, parts[3])

    return UrlDetail(parts[1], parts[2], parts[3], parts[4])


regex = re.compile("<p>(?P<description>.*)</p>", re.IGNORECASE)


def get_text_from_html(html):
    matches = regex.search(html)
    if matches is not None:
        return matches.group("description")
    else:
        return ""
