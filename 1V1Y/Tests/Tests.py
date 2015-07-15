__author__ = 'robert'

from TestHelper import TestHelper
import A1Y1V.Parsers.WebActivityLogParser as walp
from A1Y1V.Records.WebActivityRecord import WebActivityRecord

def test_line_parser_all_fields(th):
    # Id,ActionTypeId,MemberId,Created,CampaignId,TrademarkId,ProductTypeId,InventoryId,CategoryId,CustomListId,Identifier,
    # UserIp,Url,RefererUrl,UserAgentString,ExtraData
    line = "1,2,3,1/20/2012 13:53,4,5,6,7,8,9,10,212.156.132.66,http://localhost:8080/markalar/4/,REF,Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1,EXD"
    res = walp.parse_line(line)
    th.should_be(res[walp.ID], 1)
    th.should_be(res[walp.ACTION_TYPE_ID], 2)
    th.should_be(res[walp.MEMBER_ID], 3)
    th.should_be(res[walp.ACTIVITY_DATE], "1/20/2012 13:53")
    th.should_be(res[walp.CAMPAIGN_ID], 4)
    th.should_be(res[walp.TRADEMARK_ID], 5)
    th.should_be(res[walp.PRODUCT_TYPE_ID], 6)
    th.should_be(res[walp.INVENTORY_ID], 7)
    th.should_be(res[walp.CATEGORY_ID], 8)
    th.should_be(res[walp.CUSTOM_LIST_ID], 9)
    th.should_be(res[walp.IDENTIFIER], 10)
    th.should_be(res[walp.USER_IP], "212.156.132.66")
    th.should_be(res[walp.REQUESTED_URL], "http://localhost:8080/markalar/4/")
    th.should_be(res[walp.USER_AGENT], "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1")
    th.should_be(res[walp.EXTRA_DATA], "EXD")

def test_line_parser_missing_fields(th):
    # Id,ActionTypeId,MemberId,Created,CampaignId,TrademarkId,ProductTypeId,InventoryId,CategoryId,CustomListId,Identifier,UserIp,Url,RefererUrl,UserAgentString,ExtraData
    line = "1,2,3,1/20/2012 13:53,,,,,,,,1.2.3.4,,,,"
    res = walp.parse_line(line)
    th.should_be(res[walp.ID], 1)
    th.should_be(res[walp.ACTION_TYPE_ID], 2)
    th.should_be(res[walp.MEMBER_ID], 3)
    th.should_be(res[walp.ACTIVITY_DATE], "1/20/2012 13:53")
    th.should_be(res[walp.CAMPAIGN_ID], None)
    th.should_be(res[walp.TRADEMARK_ID], None)
    th.should_be(res[walp.PRODUCT_TYPE_ID], None)
    th.should_be(res[walp.INVENTORY_ID], None)
    th.should_be(res[walp.CATEGORY_ID], None)
    th.should_be(res[walp.CUSTOM_LIST_ID], None)
    th.should_be(res[walp.IDENTIFIER], None)
    th.should_be(res[walp.USER_IP], "1.2.3.4")
    th.should_be(res[walp.REQUESTED_URL], "")
    th.should_be(res[walp.USER_AGENT], "")
    th.should_be(res[walp.EXTRA_DATA], "")

def can_build_record(th):
    line = "1,2,3,1/20/2012 13:53,4,5,6,7,8,9,10,212.156.132.66,http://localhost:8080/markalar/4/,REF,Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1,EXD"
    record = WebActivityRecord(line)
    th.should_be(record.day_of_week, 4)
    th.should_be(record.category_id, 8)

if __name__ == "__main__":
    th = TestHelper()
    th.run_test(test_line_parser_all_fields)
    th.run_test(test_line_parser_missing_fields)
    th.run_test(can_build_record)
