__author__ = 'robert'


# Id,ActionTypeId,MemberId,Created,
ID = "ID"
ACTION_TYPE_ID = "ATID"
MEMBER_ID = "MID"
ACTIVITY_DATE = "CD"

# CampaignId,TrademarkId,ProductTypeId,InventoryId,CategoryId,CustomListId,
CAMPAIGN_ID = "CAMPID"
TRADEMARK_ID = "TRID"
PRODUCT_TYPE_ID = "PTID"
INVENTORY_ID = "IVID"
CATEGORY_ID = "CATID"
CUSTOM_LIST_ID = "CUSTLID"

# Identifier,UserIp,Url,RefererUrl,UserAgentString,ExtraData
IDENTIFIER = "IDENT"
USER_IP = "UIP"
REQUESTED_URL = "URL"
REFERRER = "RFER"
USER_AGENT = "UAG"
EXTRA_DATA = "EXD"

#
# CampaignId,TrademarkId,ProductTypeId,InventoryId,CategoryId,CustomListId,Identifier,UserIp,Url,RefererUrl,UserAgentString,ExtraData

def parse_line(line):
    if line == None:
        return None
    if len(line)< 15:
        return None
    if line[0] == 'I':
        return None

    parts = line.split(",")
    parsing = {}
    parsing[ID] = int(parts[0])
    parsing[ACTION_TYPE_ID] = int(parts[1])
    parsing[MEMBER_ID] = int(parts[2])
    parsing[ACTIVITY_DATE]= parts[3]

    parsing[CAMPAIGN_ID] = get_nullable_integer(parts[4])
    parsing[TRADEMARK_ID] = get_nullable_integer(parts[5])
    parsing[PRODUCT_TYPE_ID] = get_nullable_integer(parts[6])
    parsing[INVENTORY_ID] = get_nullable_integer(parts[7])
    parsing[CATEGORY_ID] = get_nullable_integer(parts[8])
    parsing[CUSTOM_LIST_ID] = get_nullable_integer(parts[9])

    parsing[IDENTIFIER] = parts[10]
    parsing[USER_IP] = parts[11]
    parsing[REQUESTED_URL] = parts[12]
    parsing[REFERRER] = parts[13]
    parsing[USER_AGENT] = parts[14]
    parsing[EXTRA_DATA] = parts[15]
    return parsing

def get_nullable_integer(val):
    if val == "":
        return None
    else:
        return int(val)
