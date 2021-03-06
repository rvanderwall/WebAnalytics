db.DA_WebLog.count() //25,728,210
db.DA_WebLog.count({Type:"videos"}) //5,153,406
db.DA_WebLog.count({Type:"videos", Description: { $exists: true, $ne:'' }})  //1,483,421
db.DA_WebLog_Videos.count() //2314854
db.DA_WebLog_Videos.count({Type:"videos", Username: { $exists: true }})
db.DA_WebLog_Videos.count({Type:"videos", Username: { $ne:'' }})
db.DA_WebLog_Videos.count({Username: { $ne:'' }})
db.DA_WebLog_Videos.aggregate({$group:{_id:"$Username",total:{$sum:1}}})
//db.DA_WebLog_Videos.update({},{$set:{Username:''}}, false, true)

db.DA_WebLog_Videos.count({Username: /admiralmemo/i})
db.DA_WebLog_Videos.find({Username: 'Eric+Costa'}, {Name:1, TimeOfRequest:1})
db.DA_WebLog_Videos.find({Username: /eddy/i}, {Name:1, TimeOfRequest:1})
db.DA_WebLog_Videos.find({Username: /james/i}, {Name:1, TimeOfRequest:1})
db.DA_WebLog_Videos.find({Username: /admiralmemo/i}, {Name:1, TimeOfRequest:1})

db.DA_WebLog_Videos.distinct('Name',{Username: /admiralmemo/i})
db.DA_WebLog_Videos.distinct('Name',{Username: /mbe/i})

db.DA_WebLog_Videos.find({Username: /admiralmemo/i}, {Name:1, TimeOfRequest:1})
db.DA_WebLog_Videos.find({Username: /rartino/i, Name:/Prisoners/i}, {Name:1, TimeOfRequest:1})





db.DA_WebLog_Videos.find({Name: '7250-Feed-Dump-100', Username: { $ne:'' }}, {Username:1, TimeOfRequest:1})



db.DA_WebLog.aggregate({$match:{Type:"videos"}},{$group:{_id:"$Type",total:{$sum:1}}})

db.DA_WebLog.find({Type:"videos", Description: { $exists: true, $ne:'' }}).limit(100)

db.DA_WebLog.find({RequestingUrl:'69.161.78.52'})

d1 = new Date(2013,8,21,4,18,11)

db.DA_WebLog_Videos.find({_id:ObjectId("52e89129785a05029c68188a")})
db.DA_WebLog.find({_id:ObjectId("52e75687785a051958709b0e")})
db.DA_WebLog.find({TimeOfRequest:d1})
