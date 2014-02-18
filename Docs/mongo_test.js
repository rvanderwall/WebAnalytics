db.TestData.find({})

db.TestData.update({},{$set:{username:''}}, false, true)

