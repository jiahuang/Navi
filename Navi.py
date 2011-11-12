#
# Navi 
# 2011 
# Jialiya Huang
#

########################################################################
# Imports
########################################################################

import flask
import shutil
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash, Response
from contextlib import closing
import os
import datetime, sys, json, time, uuid, subprocess
import bcrypt
sys.path.append("Parsers/")
from MasterParser import MasterParser
from Models import *
from operator import itemgetter
from urlparse import urlparse

########################################################################
# Configuration
########################################################################

DEBUG = True
# create app
app = Flask(__name__)
app.config.from_object(__name__)

########################################################################
# Helper functions
########################################################################
def validate_session_user():
	if 'uid' in session and 'logged_in' in session and session['logged_in']:
		return True
	return False 
	
def get_user():
	if validate_session_user():
		return db.Users.find_one({'_id':session['uid']})
	return None

def json_res(obj):
	# convert datetimes to miliseconds since epoch
	dthandler = lambda obj: time.mktime(obj.timetuple())*1000 if isinstance(obj, datetime.datetime) else None
	return Response(json.dumps(obj, default=dthandler), mimetype='application/json')

########################################################################
# Routes
########################################################################

@app.route('/error')
def error(error_msg):
	return render_template("error.html", error = error_msg)

@app.route('/')
def main():
	user = get_user()
	return render_template('main.html', user=user)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('uid', "")
	session.pop('email', "")
	flash('You were logged out')
	return redirect(url_for('main'))
	
'''
/login
	Posts
		logs in user
'''
@app.route('/login', methods=['POST'])
def login():
	
	# make sure neither value is blank
	if not request.form.get('email') or not request.form.get('password'):
		return json_res({'error':'Either the username or the password is not in our system'})
		
	user = db.Users.find_one({'email': request.form.get('email')})
	
	if not user:
		return json_res({'error':'Either the username or the password is not in our system'})
	
	hash = None
	try:
		hash = bcrypt.hashpw(request.form.get('password'), user.password)
	except:
		pass
	if hash != user.password:
		return json_res({'error':'Either the username or the password is not in our system'})
		
	session['logged_in'] = True
	session['uid'] = user._id
	session['email'] = get_user().email
	print get_user().urls
	# get list of urls
	return json_res({'loggedin':'true'})
	
'''
/new
	Posts
		creates new user
'''
@app.route('/new', methods=['POST'])
def new():
	
	# make sure neither value is blank
	if not request.form.get('email') or not request.form.get('password'):
		return json_res({'error':'Either the username or the password is not in our system'})
		
	user = db.Users()
	# check to make sure a user of that username and email doesn't already exist
	checkUser = db.Users.find_one({'email':request.form.get('email')})
	if checkUser != None:
		print "user exists"
		return json_res({'error':'User with this name already exists'})
		
	user.email = request.form.get('email')
	user.expireDays = 3 
	user.password = bcrypt.hashpw(request.form.get('password'), bcrypt.gensalt()).decode()
	user.totalNotifications = 0
	user.save()	
	
	session['logged_in'] = True
	session['uid'] = user._id
	session['email'] = user.email
		
	return json_res({'loggedin':'true'})

'''
/update
	Posts
		updates a specific url
	Gets
		returns list of updated urls
'''
@app.route('/update', methods=['POST', 'GET'])
def update():
	user = get_user()
	if user == None:
		return json_res({'error':'You must be logged in'})
	
	now = datetime.datetime.utcnow()
	if request.method == 'GET':
		# loop through list of user urls, check for any differences in notifications
		updates = []
		for url in user.urls:
			if int(url['newNotifications']) > int(url['oldNotifications']):
				updates.append(url)
		if updates:
			return json_res({'urls':updates})
		return json_res({'error':'false'})
	
	url = request.form.get("url")
	delete = request.form.get("delete")
	reset = request.form.get("reset")
	notifications = request.form.get("notifications")
	print url, reset, notifications, delete
	if reset:
		db.users.update({'email':user.email, 'urls.url':url}, 
			{'$set':{'urls.$.oldNotifications':notifications, 'urls.$.updateDate':now}})
	
	if delete:
		db.users.update({'email':user.email}, {'$pull':{'urls':{'url':url}}})
	
	return json_res({'error':'false'})
	
'''
/urls
	Posts
		adds url to user
	Gets
		returns list of added urls
'''
@app.route('/urls', methods=['GET', 'POST'])
def urls():
	
	user = get_user()
	if user == None:
		return json_res({'error':'You must be logged in'})
	
	if request.method == 'GET':
		sortedUrls = sorted(user.urls, key=itemgetter('updateDate'))
		print sortedUrls
		return json_res({'urls':sortedUrls})
		
	currTime = datetime.datetime.utcnow()
	#print request.form
	url = request.form.get("url")
	mParser = MasterParser()
	# make sure url is properly formatted
	urlparts = urlparse(url)
	if not urlparts.scheme:
		url = 'http://'+url
		urlparts = urlparse(url)
		
	# use parser and find number of current comments
	try:
		comments = mParser.parseFromUrl(url)
		expireDate = currTime + datetime.timedelta(days=user.expireDays)
		# collection update
		db.users.update({'email':user.email}, {'$push':{'urls':{
			'url':url, 'oldNotifications':comments, 
			'newNotifications':comments, 'addDate': currTime, 
			'updateDate': currTime, 'expirationDate': expireDate}}})
		# update cache
		db.cachedUrls.save({"url":url, 'comments':comments, 
			'updatedDate':currTime, 'expirationDate':expireDate})
	except:
		e = sys.exc_info()[1]
		return json_res({'error':str(e)})
	
	return json_res({'error':'false'})

@app.route('/user', methods=['GET'])
def user():
	user = get_user()
	if user == None:
		return False
	return render_template('user.html', user=user)

########################################################################
# Entry
########################################################################

if __name__ == '__main__':
	app.run()
