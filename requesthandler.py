#!/usr/bin/env python
# -*- coding: utf8 -*-

from flask import Flask 
import sys
import mysql.connector
from mysql.connector import errorcode
from flask import request
from flask import jsonify
cnx = mysql.connector.connect(user='root',
				passwd='1675',
				host='localhost',
                                database='tampon',
				charset='utf8')



from mysql.connector import errorcode

#try:
 # cnx = mysql.connector.connect(user='scott',
  #database='employ')
#except mysql.connector.Error as err:
 # if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
  #  print("Something is wrong with your user name or password")
  #elif err.errno == errorcode.ER_BAD_DB_ERROR:
   # print("Database does not exist")
  #else:
   # print(err)
#else:
 # cnx.close()

app=Flask(__name__)



@app.route("/login", methods=['GET','POST'])
def main():
	if(request.method=='POST'):
		print("afffe")
		#unArg={}		
		data=request.get_json() #username aus html post
		unArg = data.get('un')	
		pwArg = data.get('pw')
		#pwArg=request.get_json('pw') #pw aus html post
		print(unArg + " " + pwArg)
		print(type(data))
		print(data)
		#print(pwArg)
		query = "SELECT Username FROM user WHERE Username = '%s'" %(unArg,) # select username		   	
		mycursor=cnx.cursor() #DB cursor für querys
		mycursor.execute(query)
		username="";
		
		for i in mycursor:
			username = str(i[0]) #extrahierung des usernames aus query
		print(mycursor)
		query = "SELECT Passwort FROM user WHERE Username = '%s'" %(unArg,) # select passwort
		mycursor.execute(query) #query ausführung
		passwort=""
		for i in mycursor:
			passwort= str(i[0]) #extrahierung des pws
		mycursor.close()
		if (username == unArg and passwort == pwArg): #username & pw abgleich
			return jsonify(success= 'true' , messege = "login successful", status = "logged in")
		else:
			return jsonify(status = "tbd", messege = "password or username invalid", success="false")
	else:
		a = request.args.get('un')
		b = request.args.get('pw')
		query = "SELECT Username FROM user WHERE Username = '%s'" %(a,) # select username
		mycursor=cnx.cursor() #DB cursor für querys   	
		mycursor.execute(query) #query ausführung
		username="";
		for i in mycursor:
			username = str(i[0]) #extrahierung des usernames aus query
		print(mycursor)
		query = "SELECT Passwort FROM user WHERE Username = '%s'" %(a,) # select passwort
		mycursor.execute(query) #query ausführung
		passwort=""
		for i in mycursor:
			passwort= str(i[0]) #extrahierung des pws
		mycursor.close()
		if (username == a and passwort == b): #username & pw abgleich
			return jsonify(status = "logged in", success= "true", messege = "login successfull")
		else:
			return jsonify(status = "tbd", messege = "password or username invalid", success="false")
@app.route("/signup",methods=['GET', 'POST'])
def signup():
	
	mycursor= cnx.cursor()
	data = request.get_json()
	unArg = data.get('un')
	pwArg = dataget('pw')
	nameArg = data.get('name')
	mailArg = data.get('email')
	sexArg = data.get('sex')
	checkData = "SELECT count(id) from user where (Username = '%s' OR email = '%s');" %(unArg, mailArg)
	mycursor.execute(checkData)
	for i in mycursor:
		sameCount = int(i[0])
	if sameCount == 0:
		query = "INSERT INTO user (Username, Passwort, first_name, email, sex) VALUES ('%s','%s','%s','%s','%s');" %(unArg, pwArg, nameArg, mailArg, sexArg)
		mycursor.execute(query)	
		cnx.commit()
		mycursor.execute("Select * from user;")
		return jsonify(success = 'true', messege = 'signup succeeded', status = 'logged out')
	elif sameCount > 0:
		return "Username or e-Mail address already in use"
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

if __name__=="__main__":
	#sys.reload()
	#sys.setdefaultencoding('utf8')
	app.run(host="0.0.0.0", port=8080, threaded=True)
