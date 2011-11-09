import sys
sys.path.append("../Parsers/")
sys.path.append("..")
from Models import db
import datetime
from RedditParser import RedditParser

class NotificationDaemon():
	def getUrls(self, domain):
		''' returns dictionary of unique urls in domain waiting for 
		updates with the current number of notifications '''
		dbCached = list(db.CachedUrls.find({'expirationDate':{'$gte':datetime.datetime.utcnow()}, 'url':{'$regex':domain, '$options':'i'}}))
		print "db cached", dbCached
		return dbCached
	
	def updateDb(self, url, newVal):
		# update cache; using collection instead of model
		db.cachedUrls.update({"url":url}, {'$set':{'comments':newVal, 'updatedDate':datetime.datetime.utcnow()}})
		
		# update users
		db.users.update({'urls.url':url, 'urls.expirationDate':{'$lte':datetime.datetime.utcnow()}}, 
			{'$set':{'urls.$.newNotifications':newVal, 'urls.$.updateDate':datetime.datetime.utcnow()}})
