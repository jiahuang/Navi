import simplejson, urllib
from Parser import Parser
from urlparse import urlparse

class StackOverflowParser(Parser):
	def getAnswersFromUrl(self, url):
		''' returns number of answers on a particular question'''
		result = self.getResultGzip(url)
		num_answers = result['total']
		return num_answers
	
	def getNotificationsFromUrl(self, url):
		urlparts = urlparse(url)
		if urlparts.netloc != "www.stackoverflow.com" and urlparts.netloc != "stackoverflow.com":
			raise Exception, "Site is not www.stackoverflow.com"
		
		# looking for something like http://stackoverflow.com/questions/7233617/how-do-i-get-a-sum-to-calculate-properly-with-a-join
		# turn it into  http://api.stackoverflow.com/1.1/questions/7233617/answers
		resArr = filter(None, urlparts.path.split("/"))
		
		url = "http://api.stackoverflow.com/1.1/questions/"+resArr[1]+"/answers"
		return self.getAnswersFromUrl(url)
'''
s = StackOverflowParser()
url = "http://stackoverflow.com/questions/7233617/how-do-i-get-a-sum-to-calculate-properly-with-a-join"
print s.getNotificationsFromUrl(url)
'''
