__author__ = 'robert'

from datetime import datetime
import pytz

#21/Sep/2013:06:32:01 -0400
#    fmt = "%d/%b/%Y:%H:%M:%S"
#1/20/2012 13:53
#    fmt = "%m/%d/%Y:%H:%M"
def get_date_from_string_log_time(date_string):
    fmt = "%m/%d/%Y %H:%M"
    log_time = datetime.strptime(date_string, fmt)
    return log_time
