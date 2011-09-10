import sys
sys.path.append("../Parsers/")
sys.path.append("..")
from RedditParser import RedditParser
from Models import db

class RedditDaemon():
	def getUrls(self):
		''' returns dictionary of unique urls waiting for 
		updates with the current num of notifications '''
		#db.Users.find({'urls':{'expirationDate':{'$gte':datetime.datetime.now()}}})
		dbCached = db.CachedUrls.find({'expirationDate':{'$gte':datetime.datetime.now()}})
		
		#return ["http://www.reddit.com/r/worldnews/comments/k9ap8/vancouver_lawyer_gail_davidson_seeks_dick_cheneys/",
		#"http://www.reddit.com/r/worldnews/comments/k8xx8/the_palestinians_have_officially_launched_their/c2ifdtb"]
		return dbCached
	
	def updateDb(self, url, newVal):
		# update cache
		db.CachedUrls.update({"url":url}, {'$set':{'comments':newVal, 'updatedDate':datetime.datetime.now()}})
		
		# update users
		db.users.update({'urls.url':url, 'expirationDate':{'$lte':datetime.datetime.now()}}, 
			{'$set':{'urls.$.newNotifications':newVal, 'updateDate':datetime.datetime.now()}})
		
	def scrape(self):
		''' Goes through list of links to scrape and updates db'''
		parser = RedditParser()
		urls = self.getUrls()
		for url in urls:
			oldNum = url.comments
			newNum = parser.getNotificationsFromUrl(url.url)
			if oldNum > newNum:
				self.updateDb(url.url, newNum)
			print newNum

r = RedditDaemon()
r.scrape()
