# encoding: utf8
import MySQLdb

def getConn():
	return MySQLdb.connect("localhost","root","root","all",charset='utf8' )

