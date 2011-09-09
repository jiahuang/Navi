import sys
sys.path.append("../Parsers/")
sys.path.append("..")
from RedditParser import RedditParser
from Models import db

class RedditDaemon():
	def getLinks(self):
		return ["http://www.reddit.com/r/worldnews/comments/k9ap8/vancouver_lawyer_gail_davidson_seeks_dick_cheneys/",
		"http://www.reddit.com/r/worldnews/comments/k8xx8/the_palestinians_have_officially_launched_their/c2ifdtb"]
	
	def updateDb(self):
		print list(db.Users.find())
	
	def scrape(self):
		''' Goes through list of links to scrape and updates db'''
		parser = RedditParser()
		links = self.getLinks()
		for link in links:
			newNum = parser.getNotificationsFromUrl(link)
			print newNum

r = RedditDaemon()
r.scrape()
