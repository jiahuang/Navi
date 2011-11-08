import urllib2, simplejson
import zlib
import StringIO
import gzip

class Parser():
	def getResult(self, url):
		result = simplejson.load(urllib2.urlopen(url))
		if 'Error' in result:
			raise Exception, "Error retreiving results for thread "+url
		return result
	
	def getResultGzip(self, url):
		# decodes gzipped data 
		request = urllib2.Request(url)
		request.add_header('Accept-encoding', 'gzip') 
		opener = urllib2.build_opener()
		f = opener.open(request)
		compressed = StringIO.StringIO(f.read())
		gzipper = gzip.GzipFile(fileobj=compressed)
		result = simplejson.loads(gzipper.read())
		if 'Error' in result:
			raise Exception, "Error retreiving results for thread "+url
		return result
