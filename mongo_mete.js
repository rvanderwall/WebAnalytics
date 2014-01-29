db.DA_WebLog.count() //25,728,210
db.DA_WebLog.count({Type:"videos"}); //5,153,406
db.DA_WebLog.count({Type:"videos", Description: { $exists: true, $ne:'' }})  //1,483,421


db.DA_WebLog.aggregate({$match:{Type:"videos"}},{$group:{_id:"$Type",total:{$sum:1}}})
db.DA_WebLog.find({Type:"videos", Description: { $exists: true, $ne:'' }}).limit(100)


