use LogRecords
w=db.DA_WebLog

#  noon, UTC, Sept 21, 2013
d1 = new Date(2013,8,21,8,0,0)
w.find({TimeOfRequest : {$lte : d1}}).count()

resp = w.aggregate([{$match : {"TimeOfRequest" : { $lt : d1}}},
                                {$project : {"RequestingUrl" : 1}},
                                {$group : {"_id": "$RequestingUrl", "count": {$sum: 1}}}])

w.find({RequestingUrl : "162.243.4.144", Request : /username=JEdge/}, {Request : 1}).pretty()


--- git commands
git checkout -- <file>  # aborts changes
