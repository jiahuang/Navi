
import sys
sys.path.append("../Parsers/")
sys.path.append("..")
from RedditParser import RedditParser

from NotificationDaemon import NotificationDaemon
from Models import db

class RedditDaemon(NotificationDaemon):	
	def scrape(self):
		''' Goes through list of links to scrape and updates db'''
		parser = RedditParser()
		urls = self.getUrls("reddit.com")
		for url in list(urls):
			oldNum = url.comments
			newNum = parser.getNotificationsFromUrl(url.url)
			print oldNum, newNum
			if newNum > oldNum:
				self.updateDb(url.url, newNum)
			
r = RedditDaemon()
r.scrape()
