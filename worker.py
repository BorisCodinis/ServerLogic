#!/usr/bin/env python
# -*- coding: utf8 -*-


from passlib.hash import sha256_crypt
from flask import Flask 
import sys
import mysql.connector
from mysql.connector import errorcode
from flask import request
from flask import jsonify
import bcrypt

DB = mysql.connector.connect(user='root',
				passwd='1675',
				host='localhost',
                                database='tampon',
				charset='utf8')



from mysql.connector import errorcode



def getUserData(data):
	unArg = data.get('username')	
	pwArg = data.get('password')
	datajson = {'un':unArg,'pw': pwArg}
	return datajson


def executeQuery(datajson):
	DBcursor = DB.cursor()
	un = datajson.get('un')
	pw = datajson.get('pw')
	
	query = "SELECT Username FROM user WHERE Username = '%s'" %(un,) #selectUsername
	DBcursor.execute(query)
	username = ""
	for e in DBcursor:
		username = str(e[0])
	
	
	query = "SELECT Password FROM user WHERE Username = '%s'" %(un,) #selectUsername
	DBcursor.execute(query)
	password = ""
	for e in DBcursor:
		password = e[0]
	

	DBcursor.close()
	data = {'un':username, 'pw': password}
	return data

def checkLogin(dataDB, dataReq):
	
	username = dataDB.get('un')
	password = dataDB.get('pw')
	unArg = dataReq.get('un')
	pwArg = dataReq.get('pw')
	if (unArg == username and bcrypt.checkpw(pwArg.encode('utf8'), password.encode('utf8'))): #username & pw abgleich
		json = {"success": "true", "messege" : "login successful"} 
		return json
	else:
		
		json = {"success": "false", "messege" : "password or username invalid"} 
		return json

def checkUsername(query, data):
	
	unArg = data.get('un')
	pwArg = data.get('pw')
	nameArg = data.get('name')
	mailArg = data.get('email')
	sexArg = data.get('sex')
	DBcursor = DB.cursor()
	DBcursor.execute(query)
	for i in DBcursor:
		sameUserCount = int(i[0])
	if sameUserCount == 0:
		query = "INSERT INTO user (Username, Password, first_name, email, sex) VALUES ('%s','%s','%s','%s','%s');" % (unArg, bcrypt.hashpw(pwArg.encode('utf8'), bcrypt.gensalt(14)).decode('utf8'), nameArg, mailArg, sexArg)  
		print(query)
		DBcursor.execute(query)
		DB.commit()
		DBcursor.close()
		print("signup succeeded")
		return True 
		
	elif sameUserCount > 0:
		DBcursor.close()
		print("signup failed")
		return False

	
def getUserID(user):
	print("get user id: " + user)
	DBcursor = DB.cursor()
	query = "SELECT ID FROM user WHERE Username = '%s'" % (user)
	DBcursor.execute(query)
	print (DBcursor)
	uID = 0	
	for e in DBcursor:
		uID = int(e[0])
	DBcursor.close()
	print ("uID " + str(uID))
	return uID


def createDonationRecord(data):
	
	print("create donation record")
	unArg = data.get('un')
	uID = getUserID(unArg)
	DBcursor = DB.cursor()
	query = "INSERT INTO donation (userID, sum) VALUES ('%s','%s');"
	values = (getUserID(unArg), 0)	
	DBcursor.execute(query, values)
	print (DBcursor)
	DB.commit()
	DBcursor.close()
	print("donation record comitted")


def checkSignupData(data):
 
	unArg = data.get('un')
	pwArg = data.get('pw')
	nameArg = data.get('name')
	mailArg = data.get('email')
	sexArg = data.get('sex')
	query = "SELECT count(id) from user where (Username = '%s' OR email = '%s');" %(unArg, mailArg)
	if checkUsername(query, data):
		json = {"success": "true", "messege" : "signup succeeded"} 
		return json
		
	else:
		json = {"success": "false", "messege" : "signup failed"} 
		return json








