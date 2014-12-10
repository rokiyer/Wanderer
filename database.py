#!C:\Python27\python
# encoding: utf8
import sys
import MySQLdb
import time 

def insertToMysql( url , code = 0  , head = "", content = "" , error = "" ):
	conn = MySQLdb.connect("localhost","root","root","sjtuso",charset='utf8' )
	cursor = conn.cursor()
	sql = "INSERT INTO webpage ( url , code ,  head , content ,  error , fetch_time ) VALUE(%s,%s,%s,%s,%s,%s)"
	param = (url , int(code) , head , content , error , int( time.time() ) )
	cursor.execute(sql,param)
	conn.close()


def getConn():
	return MySQLdb.connect("localhost","root","root","sjtuso",charset='utf8' )

