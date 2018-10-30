#!/usr/bin/env python
# -*- coding: utf8 -*-


from flask import Flask 
import sys
import mysql.connector
from mysql.connector import errorcode
from flask import request
from flask import jsonify

DB = mysql.connector.connect(user='root',
				passwd='1675',
				host='localhost',
                                database='tampon',
				charset='utf8')




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


def getPersonalExpenseStat(un):
	DBcursor = DB.cursor()
	uId = geUserID(un)
	query = "SELCET SUM(sum) FROM expense WHERE userID = '%s'" % (uID)
	DBcursor.execute(query)
	personalSum = 0.0
	for i in DBcursor:
		personalSum = float(i[0])
	print (personalSum)
	return personalSum





def getGlobalExpenseStat():
	DBcursor = DB.cursor()
	query = "SELCET SUM(sum) FROM expense" 
	DBcursor.execute(query)
	globalSum = 0.0
	for i in DBcursor:
		globalSum = float(i[0])
	print (globalSum)
	return globalSum
