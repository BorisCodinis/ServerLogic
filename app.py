#!/usr/bin/env python
# -*- coding: utf8 -*-
import logging	
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

auth = HTTPBasicAuth()
cnx = mysql.connector.connect(user='root',
				passwd='1675',
				host='localhost',
                                database='tampon',
				charset='utf8')


app = Flask(__name__)
print("hier")
app.logger.info('in app')
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None



@app.route("/login", methods=['GET','POST'])
def main():
	print("hier2")
	app.logger.info('in login')
	if(request.method=='POST'):
		app.logger.info('in post')
		print("hier3")	
		data = request.authorization
		print(str(data))
		requestData = worker.getUserData(data)
		DBdata = worker.executeQuery(requestData)
		return worker.checkLogin(DBdata, requestData)


	else:
		return "arsch"

@app.route("/test", methods = ['GET'])
def test():
	return "Request successful!\n"
	



@app.route("/signup",methods=['GET', 'POST'])
def signup():
	
	mycursor= cnx.cursor()
	data = request.get_json()
	unArg = data.get('un')
	pwArg = data.get('pw')
	nameArg = data.get('name')
	mailArg = data.get('email')
	sexArg = data.get('sex')
	checkData = "SELECT count(id) from user where (Username = '%s' OR email = '%s');" %(unArg, mailArg)
	mycursor.execute(checkData)
	for i in mycursor:
		sameCount = int(i[0])
	if sameCount == 0:
		query = "INSERT INTO user (Username, Passwort, first_name, email, sex) VALUES ('%s','%s','%s','%s','%s');" %(unArg, base64.b64encode(pwArg), nameArg, mailArg, sexArg)
		mycursor.execute(query)	
		cnx.commit()
		
		return jsonify(success = 'true', message = 'signup succeeded', status = 'logged out')
		
	elif sameCount > 0:
		return jsonify(success = 'false', message = 'signup failes', status = 'logged out')
	mycursor.close()
@app.route("/upload",methods=['GET'])
def upload():
	mycursor = cnx.cursor()
	mycursor.execute("SELECT * FROM user;")
	stru=""
	for i in mycursor:
		stru = str(i[0])+str(i[1])+str(i[2])+str(i[3])+str(i[4])+str(i[5])+str(i[7])+str(i[8])
	mycursor.close()
	return stru
@app.route("/stats", methods=['GET'])
def getStats():
	return 1

if __name__ == "__main__":
	#sys.reload()
	#sys.setdefaultencoding('utf8')
	app.run(host="0.0.0.0", port=8080, threaded=True, debug= True, ssl_context='adhoc')
