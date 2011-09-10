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
from Models import db

########################################################################
# Configuration
########################################################################

# create app
app = Flask(__name__)
app.config.from_object(__name__)

########################################################################
# Routes
########################################################################

@app.route('/error')
def error(error_msg):
	return render_template("error.html", error = error_msg)

@app.route('/')
def main():
	# redirect logged in users
	return render_template('main.html')

# TODO: add login route

'''
/users/<username>
	Gets
		displays urls tracked by that user
		?edit displays the editing controls
	Posts
		updates user
'''
@app.route('/users/<username>')
def user(username):
	user = db.Users.find_one({'username':username.decode()})
	currTime = datetime.datetime.now()
	if request.method == 'GET':
		return render_template('user.html', user=user)
	else: # add new url
		url = request.form.get("url")
		# spin off reddit parser and find number of current comments
		mParser = MasterParser()
		comments = mParser.parseFromUrl(url)
		db.Users.update({'username':username.decode()}, {'$push':{'urls':{
			'url:url', 'oldNotifications':comments, 
			'newNotifications':comments, 'timeUpdated': currTime, 
			'expirationDate': currTime + datetime.timedelta(days=user.expireDays)}}})
		return render_template('user.html', user=user)
	return redirect(url_for('error', 'Could not find user'+username))


########################################################################
# Entry
########################################################################

if __name__ == '__main__':
	app.run()
