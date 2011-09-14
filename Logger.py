''' Logging files '''
import sys
import datetime

def log(item):
	# write data to a file
	now = datetime.datetime.now()
	filename = 'navi-'+str(now.day)+'-'+str(now.hour)+'.log'
	f = open(filename, 'a')
	f.write(str(now)+": "+str(item))
	f.close()
