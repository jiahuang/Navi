from mongokit import Connection, Document
import datetime

DATABASE = 'navi'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DEBUG = True
SECRET_KEY = 'development key'

connection = Connection(MONGODB_HOST, MONGODB_PORT)
db = connection.navi

@connection.register
class User(Document):
	__collection__ = 'users'
	__database__ = DATABASE
	structure = {
		'email' : unicode,
		'password' : unicode,
		'expireDays' : int,
		'urls' : [{'url': unicode, 'oldNotifications': int, 'newNotifications':int, 'timeUpdated':datetime.datetime}],
	}
	# ensuring unique emails
	indexes = [ 
		{ 
			'fields':['email'], 
			'unique':True, 
		} 
	]
	use_dot_notation = True 
	required_fields = ['email', 'password']
