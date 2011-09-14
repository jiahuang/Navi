import sys
sys.path.append("../Parsers/")
sys.path.append("..")
from StackOverflowParser import StackOverflowParser
from Models import db

class StackOverflowDaemon(NotificationDaemon):
	def scrape(self):
		''' Goes through list of links to scrape and updates db'''
		parser = StackOverflowParser()
		urls = self.getUrls("stackoverflow.com")
		for url in urls:
			oldNum = url.comments
			newNum = parser.getNotificationsFromUrl(url.url)
			if oldNum > newNum:
				self.updateDb(url.url, newNum)
			print newNum

s = StackOverflowDaemon()
s.scrape()
