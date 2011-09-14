import sys
sys.path.append("../Parsers/")
sys.path.append("..")
from Models import db

class NotificationDaemon():
	def getUrls(self, domain):
		''' returns dictionary of unique urls in domain waiting for 
		updates with the current num of notifications '''
		dbCached = db.CachedUrls.find({'expirationDate':{'$gte':datetime.datetime.now()}, 'url':{'$regex':domain, '$options':'i'}})
		
		return dbCached
	
	def updateDb(self, url, newVal):
		# update cache
		db.CachedUrls.update({"url":url}, {'$set':{'comments':newVal, 'updatedDate':datetime.datetime.now()}})
		
		# update users
		db.users.update({'urls.url':url, 'expirationDate':{'$lte':datetime.datetime.now()}}, 
			{'$set':{'urls.$.newNotifications':newVal, 'urls.$.updateDate':datetime.datetime.now()}})
