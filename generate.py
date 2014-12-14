import database
import re
import reg_tools

def getOutlinksString(url):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE url = %s"
	param = (url)
	cursor.execute(sql,param)
	row = cursor.fetchone()
	cursor.close()
	conn.close()
	if row == None:
		return 0
	else:
		return row[10]

def filterOutLinks(links_arr):
	allow_patterns = reg_tools.allowUrlFilter()
	deny_patterns = reg_tools.denyUrlFilter()

	proper_links = []
	for link in links_arr:
		filter_result = 1
		for pattern in allow_patterns:
			result = pattern.match(link)
			if result == None:
				filter_result = 0
				break;
		for pattern in deny_patterns:
			result = pattern.match(link)
			if result != None:
				filter_result = 0
				break;
		if filter_result:
			# remove slash
			if link != '' and link[-1] == '/':
				link = link[0:-1]
			proper_links.append(link)
	return proper_links

def checkExistUrl(links_arr):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE url = %s"
	insert_arr = []
	for link in links_arr:
		param = (link)
		result = cursor.execute(sql,param)
		if result != None:
			insert_arr.append(link)

	cursor.close()
	conn.close()
	return insert_arr

def insertIntoDB(link_arr):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "INSERT INTO webpage SET url = %s"
	for link in link_arr:
		param = (link)
		cursor.execute(sql,param)
	cursor.close()
	conn.close()
	

def updateStatus(url):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "UPDATE webpage SET status = 3 WHERE url = %s"
	param = (url)
	cursor.execute(sql,param)
	cursor.close()
	conn.close()

def generateSingleUrl(url):
	outlinks_str = getOutlinksString(url)
	if outlinks_str == 0:
		return 0;
	outlinks_arr = outlinks_str.split(',')
	proper_links = filterOutLinks(outlinks_arr)
	insert_links = checkExistUrl(proper_links)
	insertIntoDB(insert_links)
	updateStatus(url)
	print 'Generate - ' + url,
	print ' out_links:%s proper_links:%s update_links:%s'%(len(outlinks_arr)-1 , len(proper_links),len(insert_links) )
	return len(insert_links)

def generateAll(total = 100):
	print 'Generate - start to generate %s url'%(total)
	conn = database.getConn()
	cursor = conn.cursor()
	if total == 'all':
		sql = "SELECT * FROM webpage WHERE status = 2"
		param = ()
	else:
		sql = "SELECT * FROM webpage WHERE status = 2 LIMIT %s"
		param = (total)

	cursor.execute(sql,param)
	numrows = int(cursor.rowcount)
	if(numrows == 0):
		print 'Generate - Summary : All:0 New:0'
		return 0
	rows = cursor.fetchall()
	cursor.close()
	conn.close()

	cnt_udpate = 0
	for row in rows:
		url = row[1]
		cnt_udpate += generateSingleUrl(url)
	
	print 'Generate - Summary : All:%s New:%s'%(numrows,cnt_udpate)
	return 1

def check(link):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT url FROM webpage WHERE 1"
	cursor.execute(sql)
	rows = cursor.fetchall()
	for row in rows:
		print row[0]

from pybloom import BloomFilter
