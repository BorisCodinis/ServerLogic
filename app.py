#!/usr/bin/env python
# -*- coding: utf8 -*-
import logging
from passlib.hash import sha256_crypt	
from flask import Flask 
import sys
import base64
import mysql.connector
from mysql.connector import errorcode
from flask import request
from flask import jsonify
import worker
from mysql.connector import errorcode
from flask_httpauth import HTTPBasicAuth
import bcrypt
import uploader
import stats


auth = HTTPBasicAuth()
DB = mysql.connector.connect(user='root',
				passwd='1675',
				host='localhost',
                                database='tampon',
				charset='utf8')


app = Flask(__name__)
print("hier")


@auth.get_password
def get_pw(username):
	data = request.authorization
	requestData = worker.getUserData(data)
	DBdata = worker.executeQuery(requestData)
	if worker.checkLogin(DBdata, requestData):
		return data.get('password')
	else:
		return None






@app.route("/login", methods=['GET','POST'])
@auth.login_required
def main():
	print("hier2")
	#app.logger.info('in login')
	if(request.method=='POST'):
		print("logged in")
		return jsonify(success = 'true', messege = "login successful")

	else:
		return "arsch"

@app.route("/test", methods = ['GET'])
def test():
	return "Request successful!\n"
	



@app.route("/signup",methods=['GET', 'POST'])
def signup():
	
	print("signup")
	data = request.get_json()	
	messege = worker.checkSignupData(data)
	if messege['success'] == "false":
		return jsonify(messege)
	else:
		worker.createDonationRecord(data)
		return jsonify(messege)


@app.route("/up",methods=['GET'])
def upload():
	mycursor = DB.cursor()
	mycursor.execute("SELECT * FROM user;")
	stru=""
	for i in mycursor:
		stru = str(i[0])+str(i[1])+str(i[2])+str(i[3])+str(i[4])+str(i[5])+str(i[7])+str(i[8])
	mycursor.close()
	return stru

@app.route("/upload", methods = ['POST'])
@auth.login_required
def donation():
	if request.method == "POST":
		print("pictureupload")
		print(request.authorization)
		unArg = auth.username()
		print ("username: " + unArg)
		if 'file' not in request.files:
			print("no file sent")
			return "no file sent"
		else:
			picFile = request.files['file']
			if uploader.savePicture(picFile, unArg):
				return jsonify(success = 'true')
			else:
				return jsonify(success = 'false')
		
	return "banal"


@app.route("/stats", methods=['GET'])
@auth.login_required
def getStats():
	
	unArg = auth.username()
	personalSum = int(stats.getPersonalExpenseStat(unArg))
	globalSum = int(stats.getGlobalExpanseStat()) 
	
	
	return 1







if __name__ == "__main__":
	#sys.reload()
	#sys.setdefaultencoding('utf8')
	app.run(host="0.0.0.0", port=8080, threaded=True, debug= True, ssl_context='adhoc')
