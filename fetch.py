#!C:\Python27\python
# encoding: utf8
import urllib
import urllib2
import time
import database
import socket

def fetchSinglePage(url):
	request = urllib2.Request(url) 
	request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
	request.add_header('Referer', 'http://www.sjtu.edu.cn')
	request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	request.add_header('Accept-Language', 'en,zh-CN;q=0.8,zh;q=0.6')
	request.add_header('Connection', 'keep-alive')

	try:
	    response = urllib2.urlopen(request, timeout=1)
	except urllib2.HTTPError , e1:
	    response_code = e1.code
	    # code url head content error
	    return (response_code ,  '' , '' , '')
	except urllib2.URLError , e2:
		print 'Connect Error',
		return (0 , '' , '' , e2.reason)
	except socket.timeout as e3:
		print 'Connect Error',
		return (0 , '' , '' , 'time out')
	else:
		response_code = response.getcode() 
		response_url = response.geturl()
		response_head = response.info()
		response_content = response.read()
		int_code = int(response_code)
		if int_code >= 300 and int_code < 400 :
			# redirect
			return (response_code ,  '' , '' , '' )
		else :
			return (response_code , response_head , response_content , '')


def updateFetchData(url):
	result = fetchSinglePage(url)
	code = result[0]
	head = result[1]
	content = result[2]
	error = result[3]
	sql = "UPDATE webpage SET code=%s , head=%s , content=%s , error=%s , fetch_time=%s , status=1 \
		WHERE url = %s "
	param = ( int(code) , head , content , error , int( time.time() ) , url)
	conn = database.getConn()
	cursor = conn.cursor()
	res = cursor.execute(sql,param)
	cursor.close()
	conn.close()
	return res


def fetchAll(total = 100):
	conn = database.getConn()
	cursor = conn.cursor()
	if total == 'all':
		sql = "SELECT url FROM webpage WHERE status = %s "
		param = ( 0 )
	else:
		sql = "SELECT url FROM webpage WHERE status = %s LIMIT %s"
		param = ( 0 , total )
	
	cursor.execute(sql,param)
	numrows = int(cursor.rowcount)
	print 'Url waiting to fetch : %d'%(numrows)
	if numrows == 0:
		print 'No url waiting to fetch'
	else:
		rows = cursor.fetchall()
		cnt_succ = 0
		for row in rows:
			url = row[0]
			print url,
			fetch_result = updateFetchData(url)
			if fetch_result == 1:
				print 'Ok'
				cnt_succ += 1
			else:
				print 'fail'
		print 'Summary : All:%s Succ:%s Fail:%s'%(numrows , cnt_succ , numrows - cnt_succ)
	cursor.close()
	conn.close()

import info
info.showInfo()

