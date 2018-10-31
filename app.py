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
	if worker.checkLogin(DBdata, requestData) == True:
		return data.get('password')
	else:
		return jsonify(success = 'false')






@app.route("/login", methods=['GET','POST'])
@auth.login_required
def main():
	print("hier2")
	if(request.method=='POST'):
		print("logged in")
		return jsonify(success = 'true', messege = "login successful")

	else:
		return "false"

@app.route("/test", methods = ['GET'])
def test():
	return "Request successful!\n"
	



@app.route("/signup",methods=['GET', 'POST'])
def signup():
	
	print("signup")
	data = request.get_json()
	messege = worker.checkSignupData(data)
	if messege['success'] == "false":
		return jsonify(messege), 205
	else:
		worker.createDonationRecord(data)
		return jsonify(messege)


@app.route("/donation",methods=['GET','POST'])
@auth.login_required
def upload():
	print("donation")
	user = auth.username()
	donation = request.get_json()	
	value = donation.get('donationValue')
	worker.insertDonation(value, user)
	return jsonify(success ='true')

@app.route("/upload", methods = ['POST'])
@auth.login_required
def donation():
	if request.method == "POST":
		print("pictureupload")
		data = request.get_json()
		unArg = auth.username()
		
		uploader.createExpenseRecord(data, unArg)
		print ("username: " + unArg)
		
		if 'file' not in data:
			print("no file sent")
			return "no file sent"
		else:
			print("file found")
			pic = data.get('file')

			if uploader.savePicture(pic, unArg):
				return jsonify(success = 'true')
			else:
				return jsonify(success = 'false')
		
	return "banal"


@app.route("/stats", methods=['GET'])
@auth.login_required
def getStats():
	
	data = request.authorization
	unArg = data.get('username')
	print(unArg)

	
	

	

	
	return jsonify(success = "e", expenseItems = "{\"amount\":\"h\", \"date\":\"h\", \"description\":\"h\"}", donationItems = "{\"amount\":\"h\", \"date\":\"h\"}"), 200







if __name__ == "__main__":
	#sys.reload()
	#sys.setdefaultencoding('utf8')
	app.run(host="0.0.0.0", port=8080, threaded=True, debug= True, ssl_context='adhoc')
