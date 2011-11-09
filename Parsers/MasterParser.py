from urlparse import urlparse
from RedditParser import RedditParser

class MasterParser():
	def __init__(self):
		self.redditParser = RedditParser()
		
	def parseFromUrl(self, url):
		urlparts = urlparse(url)
		if urlparts.netloc == "www.reddit.com":
			return int(self.redditParser.getNotificationsFromUrl(url))
		# TODO: Add other parsers
			
		raise Exception, "Site is not reddit.com"
	
'''
m = MasterParser()
url = "http://www.reddit.com/r/worldnews/comments/k9ap8/vancouver_lawyer_gail_davidson_seeks_dick_cheneys/"
print m.parseFromUrl(url)
url = "http://www.reddit.com/r/worldnews/comments/k8xx8/the_palestinians_have_officially_launched_their/c2ifdtb"
print m.parseFromUrl(url)
'''
