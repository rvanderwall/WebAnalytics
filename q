diff --git a/SimpleStats.py b/SimpleStats.py
index cf8dad6..9cd882f 100644
--- a/SimpleStats.py
+++ b/SimpleStats.py
@@ -14,28 +14,45 @@ def get_simple_stats(logCollection):
 
     other_stats = True
     if other_stats:
-        resp = logCollection.aggregate([{"$group": {"_id": "$Verb", "count": {"$sum": 1}}}])
-        print "Verbs:"
-        print resp["result"]
-
-        resp = logCollection.aggregate([{"$group": {"_id": "$Status", "count": {"$sum": 1}}}])
-        print "Status Codes:"
-        print resp["result"]
-
-        resp = logCollection.aggregate([{"$project": {fn.REQUESTING_URL: 1}},
-                                         {"$group": {"_id": "$" + fn.REQUESTING_URL}}])["result"]
-        print "Unique requestors: %d" % (len(resp))
-
-
-        resp = logCollection.aggregate([{"$group": {"_id": "$" + fn.REFERRER}}])
+        if False:   #Already recored, don't need to run each time.
+            resp = logCollection.aggregate([{"$group": {"_id": "$Verb", "count": {"$sum": 1}}}])
+            print "Verbs:"
+            print resp["result"]
+
+            resp = logCollection.aggregate([{"$group": {"_id": "$Status", "count": {"$sum": 1}}}])
+            print "Status Codes:"
+            print resp["result"]
+
+            #  Try with standard aggregate -- I get 'Doc too big' error
+            #resp = logCollection.aggregate([{"$project": {fn.REQUESTING_URL: 1}},
+            #                                 {"$group": {"_id": "$" + fn.REQUESTING_URL}}])["result"]
+            #print "Unique requestors: %d" % (len(resp))
+
+            # Try with distinct -- Still get 'Doc too big'
+            #resp = logCollection.distinct(fn.REQUESTING_URL)
+            #print "Unique requestors: %d" % resp.count()
+
+            # Try within the pipeline
+            resp = logCollection.aggregate([{"$project": {fn.REQUESTING_URL: 1}},
+                                            {"$group": {"_id": "$" + fn.REQUESTING_URL}},
+                                            {"$group": {"_id": 1, "count": { "$sum" : 1}}}])
+            print "Unique requestors:"
+            print resp
+
+        resp = logCollection.aggregate([{"$project": {fn.REFERRER: 1}},
+                                            {"$group": {"_id": "$" + fn.REFERRER}},
+                                            {"$group": {"_id": 1, "count": { "$sum" : 1}}}])
         print "Unique referrers:"
-        print len(resp["result"])
+        print resp["result"]
 
         regx = re.compile("escapistmagazine", re.IGNORECASE)
         check = {"Referrer": regx}
-        resp = logCollection.aggregate([{"$match": check}, {"$group": {"_id": "$" + fn.REFERRER}}])
+        resp = logCollection.aggregate([{"$match": check},
+                                        {"$project": {fn.REFERRER: 1}},
+                                        {"$group": {"_id": "$" + fn.REFERRER}},
+                                        {"$group": {"_id": 1, "count": { "$sum" : 1}}}])
         print "Escapist referrers:"
-        print len(resp["result"])
+        print resp["result"]
 
         regx = re.compile("gurl", re.IGNORECASE)
         check = {"Referrer": regx}
