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
	return Response(json.dumps(obj), mimetype='application/json')

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
	
	return json_res({'loggedin':'true'})
	
'''
/new
	Posts
		creates new user
'''
@app.route('/new', methods=['POST'])
def new():
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
	session['email'] = request.form['email']
		
	return json_res({'loggedin':'true'})
	
'''
/urls
	Posts
		adds url to user
'''
@app.route('/urls', methods=['POST'])
def urls():
	
	user = get_user()
	if user == None:
		return json_res({'error':'You must be logged in for submitting urls'})
		
	currTime = datetime.datetime.now()
	print request.form
	url = request.form.get("url")
	# use parser and find number of current comments
	mParser = MasterParser()
	try:
		comments = mParser.parseFromUrl(url)
		expireDate = currTime + datetime.timedelta(days=user.expireDays)
		# collection update
		db.users.update({'email':user.email}, {'$push':{'urls':{
			'url':url, 'oldNotifications':comments, 
			'newNotifications':comments, 'updateDate': currTime, 
			'expirationDate': expireDate}}})
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
