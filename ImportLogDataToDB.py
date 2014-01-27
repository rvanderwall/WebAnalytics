__author__ = 'rlv'

import sys
import urllib2
import xml.etree.ElementTree as ET
from datetime import datetime

from LogFileHelper import get_text_from_html, check_url_for_video, add_description
from VideoInfoRecord import VideoInfoRecord
from LogRecord import LogRecord
from CDNRecord import CDNRecord


def import_log_data_to_repo(repo, log_file, skip_rows=1, max_rows=sys.maxint, only_videos=False, descriptions=None):
    f = open(log_file, 'r')
    line_num = 0
    repo.drop_collection()

    for line in f:
        line_num += 1
        log_record = LogRecord(line)
        if log_record.all_data_valid:
            if line_num % 100000 == 0:
                print "PROCESSING LINE {0}".format(line_num)
            if line_num % skip_rows == 0:
                # if only_videos:
                #     if descriptions is not None and check_url_for_video(log_record):
                #         add_description(log_record, descriptions)
                #         try:
                #             repo.insert_record(log_record)
                #         except Exception:
                #             print "ERROR INSERTING LINE {0}".format(line_num)
                #             print line
                # else:
                #     try:
                #         repo.insert_record(log_record)
                #     except Exception:
                #         print "ERROR INSERTING LINE {0}".format(line_num)
                #         print line

                if descriptions is not None:
                    add_description(log_record, descriptions)
                try:
                    repo.insert_record(log_record)
                except Exception:
                    print "ERROR INSERTING LINE {0}".format(line_num)
                    print line
        else:
            print "ERROR in line {0}".format(line_num)
        if line_num > max_rows:
            break
    print "PROCESSED {0} LINES".format(line_num)


def import_cdn_data_to_repo(repo, log_file, skip_rows=1, max_rows=sys.maxint):
    f = open(log_file, 'r')
    line_num = 0
    repo.drop_collection()

    for line in f:
        line_num += 1
        cdn_record = CDNRecord(line)
        if cdn_record.all_data_valid:
            if line_num % 100000 == 0:
                print "PROCESSING LINE {0}".format(line_num)
            if line_num % skip_rows == 0:
                try:
                    repo.insert_record(cdn_record)
                except Exception:
                    print "ERROR INSERTING LINE {0}".format(line_num)
                    print line
        else:
            print "ERROR PARSING LINE {0}".format(line_num)
        if line_num > max_rows:
            break
    print "PROCESSED {0} LINES".format(line_num)


def import_video_information_to_repo(repo):
    repo.drop_collection()
    record_num = 0
    for xml_index in range(1, 203):
        try:
            response = urllib2.urlopen("http://www.escapistmagazine.com/rss/videos/list/" + str(xml_index) + ".xml")
        except:
            continue
        xml_raw = response.read()
        if not xml_raw:
            continue
        root = ET.fromstring(xml_raw)

        for channel in root.findall("./channel"):
            channel_title = channel.find("title").text
            channel_description = channel.find("description").text
            print channel_title
            for item in channel.findall("item"):
                record = VideoInfoRecord()
                record.xml_index = xml_index
                record.channel = channel_title
                record.channel_description = channel_description

                record.title = item.find("title").text
                record.link = item.find("link").text
                record.description = get_text_from_html(item.find("description").text)
                record.category = item.find("category").text
                record.pubdate = datetime.strptime(item.find("pubDate").text, "%a, %d %b %Y %H:%M:%S %Z")
                record.creator = item.find("{http://purl.org/dc/elements/1.1/}creator").text
                record_num += 1


                try:
                    repo.insert_record(record)
                except Exception:
                    print "ERROR INSERTING LINE {0}".format(record_num)
                    print record.title, record.link, record.description, record.pubdate

                print record.title, record.link, record.description, record.pubdate

    print "PROCESSED {0} VIDEO DESCRIPTIONS".format(record_num)

