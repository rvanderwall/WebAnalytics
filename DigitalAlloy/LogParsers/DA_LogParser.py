__author__ = 'robert'

import re

import DigitalAlloy.Records.FieldNames as fn

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

def parse_apache_data_line(line):
    groups = try_regex1(line)
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
    data = parse_apache_data_line(logLine)
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
    data = parse_apache_data_line(logLine)
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
