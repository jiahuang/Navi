import simplejson, urllib
from Parser import Parser
from urlparse import urlparse

class RedditParser(Parser):
	def getCommentsFromThread(self, url):
		result = self.getResult(url)
			
		num_comments = result[0]['data']['children'][0]['data']['num_comments']
		if num_comments == '':
			num_comments = 0
		return int(num_comments)
		
	def getRepliesFromComment(self, url):
		result = self.getResult(url)
			
		num_replies = result[1]['data']['children'][0]['data']['replies']
		if num_replies == '':
			num_replies = 0
		return int(num_replies)
		
	def getNotificationsFromUrl(self, url):
		''' Takes in a link from reddit and returns number of comments'''
		urlparts = urlparse(url)
		if urlparts.netloc != "www.reddit.com" and urlparts.netloc != "reddit.com":
			raise Exception, "Site is not www.reddit.com"
		
		# check if url is thread or comment
		resArr = filter(None, urlparts.path.split("/"))
		
		url = url + ".json" if url[-1] == '/' else url+"/.json"
		
		if len(resArr) == 5:
			return self.getCommentsFromThread(url)
		elif len(resArr) == 6:
			return self.getRepliesFromComment(url)
		
		raise Exception, "Path was: "+urlparts.path
'''
r = RedditParser()
url = "http://www.reddit.com/r/worldnews/comments/k9ap8/vancouver_lawyer_gail_davidson_seeks_dick_cheneys/"
print r.getNotificationsFromUrl(url)
url = "http://www.reddit.com/r/worldnews/comments/k8xx8/the_palestinians_have_officially_launched_their/c2ifdtb"
print r.getNotificationsFromUrl(url)
'''
