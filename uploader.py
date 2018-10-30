import mysql.connector
from mysql.connector import errorcode
from flask import request
from flask import jsonify
import time
import datetime

DB = mysql.connector.connect(user='root', passwd='1675', host='localhost', database='tampon', charset='utf8')
upload_folder = "/home/b/tamapp/uploads"

def createFilename(un):
	DBcursor = DB.cursor()
	query = "SELECT ID FROM user WHERE Username = '%s'" % (un)
	DBcursor.execute(query)
	for i in DBcursor:
		uID = int(i[0])
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	st = st.replace(" ","")
	fileName = str(uID) + "_" + st
	print (fileName)
	DBcursor.close()
	return fileName



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





def createDBRecord(filename, un):
	
	
	DBcursor = DB.cursor()
	query = "INSERT INTO picture (userID, path) VALUES (%s, %s)"
	uID = getUserID(un)
	values = (uID, (upload_folder + "/" + filename))	
	DBcursor.execute(query, values)
	print(DBcursor)
	DB.commit()
	print("")


def savePicture(picFile, un):
	filename = createFilename(un)
	
	file.save(os.path.join(upload_folder, filename))
	createdDBRecord(filename, un)
	return True

