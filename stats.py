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
	uID = 0	
	for e in DBcursor:
		uID = int(e[0])
	DBcursor.close()
	print ("uID " + str(uID))
	
	return uID


def getPersonalExpenseStat(un):
	
	DBcursor = DB.cursor()
	uID = getUserID(un)
	query = "SELECT SUM(sum) FROM expense WHERE userID = '%s'" % (uID)
	DBcursor.execute(query)
	personalSum = 0.0
	for i in DBcursor:
		personalSum = float(i[0])
	
	DBcursor.close()
	print (personalSum)
	return personalSum





def getGlobalExpenseStat():
	
	DBcursor = DB.cursor()
	query = "SELECT SUM(sum) FROM expense" 
	DBcursor.execute(query)
	globalSum = 0.0
	for i in DBcursor:
		globalSum = float(i[0])
	print (globalSum)
	
	DBcursor.close()
	return globalSum



def getPersonalDonationStat(un):
	
	DBcursor = DB.cursor()
	uID = getUserID(un)
	query = "SELECT SUM(sum) FROM donation WHERE userID = '%s'" % (uID)
	DBcursor.execute(query)
	personalSum = 0.0
	for i in DBcursor:
		personalSum = float(i[0])
	print (personalSum)
	
	
	DBcursor.close()
	return personalSum





def getGlobalDonationStat():
	
	DBcursor = DB.cursor()
	query = "SELECT SUM(sum) FROM donation" 
	DBcursor.execute(query)
	globalSum = 0.0
	for i in DBcursor:
		globalSum = float(i[0])
	print (globalSum)
	
	DBcursor.close()
	return globalSum
	

def fillJson(cursor, jdict, a):



	if a == 0:
		jdict["amount"] = cursor
	if a == 1:
		jdict["description"] = cursor[1]
	if a == 2:
		jdict["date"] = cursor[2]

	return jdict

def getExpenses(un):
	DBcursor = DB.cursor()
	uID = getUserID(un)
	query = "SELECT count(ID) FROM expense WHERE userID = %s" % (uID)
	DBcursor.execute(query)
	n = 0;
	for i in DBcursor:
		n = int(i[0])
	print(str(n) + " erg.")
	query = "SELECT  sum, article, datetime FROM expense WHERE userID = %s" %(uID)
	DBcursor.execute(query)
	print("22222")

	print("3333333")
	jdict = {"amount":"0", "description":"a", "date":"a"}
	for i in DBcursor:
		a = 0
		jdict = fillJson(i,jdict, a)
		a = a+1
	print (jdict)
	DBcursor.close()
	DBcursor.close()
	DB.cmd_reset_connection()




