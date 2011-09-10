from mongokit import Connection, Document
import datetime

DATABASE_NAVI = 'navi'
DATABASE_CACHED = 'navi_cached'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DEBUG = True
SECRET_KEY = 'development key'

connection = Connection(MONGODB_HOST, MONGODB_PORT)
db = connection.navi

@connection.register
class Users(Document):
	__collection__ = 'users'
	__database__ = DATABASE_NAVI
	structure = {
		'email' : unicode,
		'username': unicode,
		'password' : unicode,
		'expireDays' : int,
		'urls' : [{'url': unicode, 
					'oldNotifications': int, 
					'newNotifications':int, 
					'updateDate':datetime.datetime,
					'expirationDate': datetime.datetime}],
		'totalNotifications' : int,
	}
	# ensuring unique emails
	indexes = [ 
		{ 
			'fields':['email', 'username'], 
			'unique':True, 
		} 
	]
	use_dot_notation = True 
	required_fields = ['email', 'username', 'password']

@connection.register
class CachedUrls(Document):
	__collection__ = 'cachedUrls'
	__database__ = DATABASE_NAVI
	structure = {
		'url' : unicode,
		'updateDate' : datetime.datetime,
		'comments' : int, # number of things being tracked for notification
		'expirationDate': datetime.datetime,
	}
	# ensuring unique urls
	indexes = [ 
		{ 
			'fields':['url'], 
			'unique':True, 
		} 
	]
	use_dot_notation = True 
	required_fields = ['url']
