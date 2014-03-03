__author__ = 'rlv'

import re
from datetime import timedelta, datetime
import collections
from pytz import timezone
import pytz

from DigitalAlloy.Records import FieldNames as fn


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


def get_os_from_agent(agent):
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


#21/Sep/2013:06:32:01 -0400
def get_date_from_string_log_time(date_string):
    fmt = "%d/%b/%Y:%H:%M:%S"
    log_time = datetime.strptime(date_string[:-6], fmt)
    log_timezone = timezone("Etc/GMT+4")
    loc_log_time = log_timezone.localize(log_time)
    utc_log_time = loc_log_time.astimezone(pytz.utc)
    return utc_log_time


#21/Sep/2013:00:00:00 +0000
def get_date_from_string_cdn_time(date_string):
    fmt = "%d/%b/%Y:%H:%M:%S"
    log_time = datetime.strptime(date_string[:-6], fmt)
    log_timezone = pytz.utc
    utc_log_time = log_timezone.localize(log_time)
    return utc_log_time


def get_date_from_string_2(date_string, offset):
    try:
        offset = int(date_string[-5:])
    except Exception:
        print "Error"

    fmt = "%d/%b/%Y:%H:%M:%S"
    delta = timedelta(hours=offset / 100)
    log_time = datetime.strptime(date_string[:-6], fmt)
    log_time -= delta
    return log_time


#regex_url = re.compile("(?:\w*)\s/(?P<type>\w*)/(?P<type2>\w*)(?:/(?P<section>.*))?/(?P<name>.*$)", re.IGNORECASE)
#regex_url = re.compile("(?:\w*)\s/(?P<type>\w*)/(?P<type2>\w*)(?:/(?P<section>[^ \s]*))?/(?P<name>[^ \s]*)", re.IGNORECASE)
regex_url = re.compile("/(?P<type>\w*)/(?P<type2>\w*)(?:/(?P<section>[^ \s]*))?/(?P<name>[^ \s]*)", re.IGNORECASE)


def get_url_details(request):
    url_detail = collections.namedtuple('url_detail', 'type type2 section name')
    #o = urlparse(request)
    #path = o.path
    matches = re.match('GET (.*) HTTP/1.[01]', request)
    if matches is None:
        return url_detail(None, None, None, None)
    request_path = matches.groups()[0]
    path = request_path.split('?')[0]
    parts = path.split('/')

    if len(parts) == 1:   # /
        return url_detail(None, None, None, None)
    if len(parts) == 2:   # /t
        return url_detail(parts[1], None, None, None)
    if len(parts) == 3:   # /t/u
        return url_detail(parts[1], parts[2], None, None)
    if len(parts) == 4:   # /t/u/v
        return url_detail(parts[1], parts[2], None, parts[3])

    return url_detail(parts[1], parts[2], parts[3], parts[4])


regex_html = re.compile("<p>(?P<description>.*)</p>", re.IGNORECASE)


def get_text_from_html(html):
    matches = regex_html.search(html)
    if matches is not None:
        return matches.group("description")
    else:
        return ""


regex_video = re.compile("(?P<videos>^GET /videos/view/\S+/\S+$|^GET /videos/view/\S+/\S+\s.+$)", re.IGNORECASE)


def check_url_for_video(log_record):
    url = log_record.request
    matches = regex_video.search(url)
    if matches is None:
        return False

    return True


def get_title_and_description(video_info):
    title = re.sub(ur"['\-().,:&\" ]", "", video_info[fn.VIDEO_TITLE], 0, re.UNICODE).lower()
    description = re.sub(ur"<.+?>", "", video_info[fn.VIDEO_DESCRIPTION], 0, re.UNICODE)
    return title, description


regex_title = re.compile(ur"\d+-(?P<title>\b.+\b)", re.IGNORECASE | re.UNICODE)
regex_title_replace = re.compile(ur"['\-().,: ]", re.IGNORECASE | re.UNICODE)


def add_description(log_record, descriptions):
    if log_record.name is not None:
        matches = regex_title.search(log_record.name)
        if matches is not None:
            fixed_title = re.sub(regex_title_replace, "", matches.group("title"), 0).lower()
            try:
                log_record.fixed_name = fixed_title
                log_record.description = descriptions[unicode(fixed_title)]
            except KeyError:
                # print "Cannot find the description for the video --> {0}".format(log_record.name)
                pass

# Pull user name from request of this form:
# "/rss/videos/podcast/1.xml?username=thisisthechris&xid=92a1bef8aa9861d8e66eba"
def extractUserNameFromRequest(request):
    params = request.split('?')
    if len(params) < 2:
        return None
    userParam = params[1].split('&')[0]
    fieldValue = userParam.split('=')
    if fieldValue[0] == "username":
        return fieldValue[1]
    else:
        return None
