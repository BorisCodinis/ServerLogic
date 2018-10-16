
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



def getUserData(data):
	unArg = data.get('username')	
	pwArg = data.get('password')
	print(unArg + " " + pwArg)
	print(data)
	datajson = {'un':unArg,'pw': pwArg}
	return datajson


def executeQuery(datajson):
	DBcursor = cnx.cursor()
	un = datajson.get('un')
	pw = datajson.get('pw')
	
	query = "SELECT Username FROM user WHERE Username = '%s'" %(un,) #selectUsername
	DBcursor.execute(query)
	username = ""
	for e in DBcursor:
		username = str(e[0])
	
	
	query = "SELECT Passwort FROM user WHERE Username = '%s'" %(un,) #selectUsername
	DBcursor.execute(query)
	password = ""
	for e in DBcursor:
		password = str(e[0])
	

	DBcursor.close()
	data = {'un':username, 'pw': password}
	return data

def checkLogin(dataDB, dataReq):
	
	username = dataDB.get('un')
	password = dataDB.get('pw')
	unArg = dataReq.get('un')
	pwArg = dataReq.get('pw')
	#print(username +" "+ password)
	#print(unArg + " " + pwArg)
	if (username == unArg and password == pwArg): #username & pw abgleich
		return jsonify(success= 'true' , messege = "login successful", status = "logged in")
	else:
		return jsonify(status = "tbd", messege = "password or username invalid", success="false")





