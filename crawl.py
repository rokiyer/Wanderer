#!C:\Python27\python
# encoding: utf8
import urllib
import urllib2
import time
import database

def crawlSinglePage(url):
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
	    return (response_code ,  None , None , None)
	except urllib2.URLError , e2:
		return (None , None , None , e2.reason)
	else:
		response_code = response.getcode() 
		response_url = response.geturl()
		response_head = response.info()
		response_content = response.read()
		int_code = int(response_code)
		if int_code >= 300 and int_code < 400 :
			# redirect
			return (response_code ,  None , None , None )
		else :
			return (response_code , response_head , response_content , None)


def updateFetchData(url):
	result = crawlSinglePage(url)
	code = result[0]
	head = result[1]
	content = result[2]
	error = result[3]
	sql = "UPDATE webpage SET code=%s , head=%s , content=%s , error=%s , fetch_time=%s \
		WHERE url = %s "
	param = ( int(code) , head , content , error , int( time.time() ) , url)
	conn = database.getConn()
	cursor = conn.cursor()
	res = cursor.execute(sql,param)
	cursor.close()
	conn.close()
	print res


def crawl(total = 100):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT url FROM webpage WHERE status = %s LIMIT %s"
	param = ( 0 , total )
	cursor.execute(sql,param)
	numrows = int(cursor.rowcount)
	print 'Url waiting to fetch : %d'%(numrows)
	if numrows > 0:
		rows = cursor.fetchall()
		for row in rows:
			url = row[0]
			print url
			updateFetchData(url)
	conn.close()

crawl()

