#!C:\Python27\python
# encoding: utf8
import urllib
import urllib2
import time
import database
import socket

def getRequest(url):
	request = urllib2.Request(url) 
	request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
	request.add_header('Referer', 'http://www.sjtu.edu.cn')
	request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	request.add_header('Accept-Language', 'en,zh-CN;q=0.8,zh;q=0.6')
	request.add_header('Connection', 'keep-alive')
	return request

def getResponse(request):
	
	try:
	    response = urllib2.urlopen(request, timeout=1)
	except urllib2.HTTPError , e1:
	    response = {
		'code':e1.code, # like 404
		'head':'',
		'content':'',
		'error_msg':''
		}
	except urllib2.URLError , e2:
		response = {
		'code':0 ,
		'head':'',
		'content':'',
		'error_msg':'connect error'
		}
	except socket.timeout as e3:
		response = {
		'code':0 ,
		'head':'',
		'content':'',
		'error_msg':'time out'
		}
	else:
		response = {
		'code':response.getcode() ,
		'head':response.info() ,
		'content':response.read(),
		'error_msg':''
		}
	return response


def update(url, response):
	if response['code'] == 200:
		status = 1
	else:
		status = 10

	sql = "UPDATE webpage SET code=%s , head=%s , content=%s , error=%s , fetch_time=%s , status=1 \
		WHERE url = %s "
	
	error_msg = response[3]
	param = ( response['code'] , response['head'] , response['content'] , response['error_msg'] , time.time() , url)
	conn = database.getConn()
	cursor = conn.cursor()
	update_result = cursor.execute(sql,param)
	cursor.close()
	conn.close()
	return update_result


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
	numrows = cursor.rowcount
	cnt_succ = 0
	print 'Fetch - Url waiting to fetch : %d ...'%(numrows)
	if numrows != 0:
		rows = cursor.fetchall()
		for row in rows:
			url = row[0]
			request = getRequest(url)
			response = getResponse(request)
			if response['code'] == 200:
				++cnt_succ
				print 'fetch succ ',
			else:
				print 'fetch fail ',
			print url
			result = updateFetchData(url,response)
			if result == 0:
				print 'update error'
			
		
	cursor.close()
	conn.close()
	print 'Summary : All:%s Succ:%s Fail:%s'%(numrows , cnt_succ , numrows - cnt_succ)
	return {'all':numrows,'succ':cnt_succ,'fail':numrows - cnt_succ}

import info
info.showInfo()

