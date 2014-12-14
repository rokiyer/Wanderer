#!C:\Python27\python
# -*- coding: utf-8 -*-  
import urllib
import urllib2
import time
import database
import socket
import chardet

def getRequest(url):
	# set time out = 5s
	socket.setdefaulttimeout(30)

	request = urllib2.Request(url) 
	request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
	request.add_header('Referer', 'http://www.sjtu.edu.cn')
	request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	request.add_header('Accept-Language', 'en,zh-CN;q=0.8,zh;q=0.6')
	request.add_header('Connection', 'keep-alive')
	return request

def getResponse(request):
	
	try:
	    response = urllib2.urlopen(request)
	except urllib2.HTTPError , e1:
	    result = {
		'code':e1.code, # like 404
		'head':'',
		'content':'',
		'error_msg':''
		}
	except urllib2.URLError , e2:
		result = {
		'code':0 ,
		'head':'',
		'content':'',
		'error_msg':'connect error'
		}
	except socket.timeout , e3:
		result = {
		'code':0 ,
		'head':'',
		'content':'',
		'error_msg':'time out'
		}
	except :
		result = {
		'code':0 ,
		'head':'',
		'content':'',
		'error_msg':'Unknown error'
		}
	else:
		head = response.info()
		code = response.getcode()
		# refuse large page
		if 'Content-Length' in head and int(head['Content-Length']) > 524288: # 512K
			result = {
			'code':code,
			'head':head,
			'content':'',
			'error_msg':'Content too large'
			}
			return result

		# try to find out pageset like html/text
		content_type = head['Content-type'].lower()
		if content_type.find('charset=') == -1:
			pageset = content_type
			charset = ''
		else:
			index = content_type.rindex(';')
			pageset = content_type[0:index]
			index = content_type.rindex('=')
			charset = content_type[index+1:index+len(content_type)]

		if pageset != 'text/html' :
			result = {
			'code':code,
			'head':head,
			'content':'',
			'error_msg':'Content type not text/html'
			}
			return result

		# try to find out charset like gbk 
		content = response.read()
		if charset == '':
			char_det = chardet.detect(content)
			charset = char_det['encoding']

		# print pageset
		# print charset

		# make encoding right
		if charset != 'utf-8' and charset != 'UTF-8':
			try:
				content = content.decode(charset).encode('utf-8')
				error_msg = ''
			except:
				content = ''
				error_msg = 'Decode content error'
		
		# print content

		result = {
		'code':code,
		'head':head,
		'content':content,
		'error_msg':''
		}
		return result
	#exception return 
	return result


def update(url, response):
	# prepare the data to put into database
	code = int(response['code'])
	head = response['head']
	content = response['content']
	error_msg = response['error_msg']
	fetch_time = int(time.time())
	status = 10
	if response['code'] == 200 and response['error_msg'] == '':
		status = 1

	sql = "UPDATE webpage SET `code`=%s , `head`=%s , `status`=%s , \
	`content`=%s , `error`=%s , `fetch_time`=%s \
	 WHERE `url` =%s "
	param = (code,head,status,content,error_msg,fetch_time,url)
	conn = database.getConn()
	cursor = conn.cursor()
	update_result = cursor.execute(sql,param)
	cursor.close()
	conn.close()
	return update_result

def fetchSingle(url):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE url = %s"
	param = (url)
	cursor.execute(sql,param)
	numrows = cursor.rowcount
	if numrows == 0:
		print 'Url is not in database , inject first'
		return False
	else:
		print url,
		request = getRequest(url)
		response = getResponse(request)
		result = update(url,response)

		if response['code'] == 200 and response['error_msg'] == '':
			cnt_succ += 1
			print 'fetch succ '
		else:
			print 'fetch fail '
		
		return True

def fetchAll(total = 100):
	print 'Fetch - Start... %s urls'%(total)
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
	if numrows != 0:
		rows = cursor.fetchall()
		for row in rows:
			url = row[0]
			print 'Fetch - '+url,
			request = getRequest(url)
			response = getResponse(request)
			update(url,response)

			if response['code'] == 200 and response['error_msg'] == '':
				cnt_succ += 1
				print 'fetch succ '
			else:
				print 'fetch fail '

	cursor.close()
	conn.close()
	print 'Fetch - Summary : All:%s Succ:%s Fail:%s'%(numrows , cnt_succ , numrows - cnt_succ)
	return {'all':numrows,'succ':cnt_succ,'fail':numrows - cnt_succ}

