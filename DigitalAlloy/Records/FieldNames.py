__author__ = 'robert'

from config import CUSTOMER

#
# Names of the Database collections
#
COLLECTION_WEBLOG = CUSTOMER + "_WebLog"
COLLECTION_WEBLOG_SPARCE = CUSTOMER + "WebLog_Sparce"
COLLECTION_CDNLOG = CUSTOMER + "_CDNLog"
COLLECTION_CDNLOG_SPARCE = CUSTOMER + "_CDNLog_Sparce"
COLLECTION_VIDEO_INFO = CUSTOMER + "_Video_Info"
COLLECTION_VIDEO_WEB_LOG = CUSTOMER + "_WebLog_Videos"


#
#   Names of the fields in the database
REQUESTING_URL = "RequestingUrl"
DATETIME_OF_REQUEST = "TimeOfRequest"
TIME_OF_REQUEST = "TimeOnlyOfRequest"
DAY_OF_WEEK = "DayOfWeek"

URL = "URL"
REMOTE_LOG_NAME = "RemoteLogName"
REMOTE_USER = "RemoteUser"
REQUEST = "Request"
HTTP_VERB = "Verb"
HTTP_STATUS = "Status"

BYTES_SENT = "Bytes"
REFERRER = "Referrer"
USER_AGENT = "UserAgent"
USER_OS = "OS"
USER_BROWSER = "Browser"

# Fields found only in the WebLog
DATA_ID = "_id"
DATA_TYPE = "Type"
DATA_SUBTYPE = "Type2"
DATA_SECTION = "Section"
DATA_NAME = "Name"
DATA_FIXED_NAME = "FixedName"
DATA_DESCRIPTION = "Description"
DATA_USERNAME = "Username"

MOZILLA_PARAMS = "MozillaParameters"
UNIQUE_ID = "UniqueId"

MEMORY_USE = "MemoryUse"
PROCESSING_TIME = "ProcessingTime"



#
# Fields from the Video
CHANNEL_INDEX = "index_num"
CHANNEL_TITLE = "channel_title"
CHANNEL_DESCRIPTION = "channel_description"
VIDEO_TITLE = "video_title"
VIDEO_LINK = "link"
VIDEO_DESCRIPTION = "video_description"
VIDEO_USERNAME = "username"
PUB_DATE = "Pubdate"
VIDEO_CREATOR = "video_creator"
VIDEO_CATEGORY = "video_category"