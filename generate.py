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

def update(links_arr):
	conn = database.getConn()
	cursor = conn.cursor()
	sql1 = "SELECT * FROM webpage WHERE url = %s"
	sql2 = "INSERT INTO webpage SET url = %s"
	cnt_udpate = 0
	for link in links_arr:
		param = (link)
		cursor.execute(sql1,param)
		if cursor.rowcount == 0:
			#insert link into page 
			cursor.execute(sql2,param)
			cnt_udpate += 1
	cursor.close()
	conn.close()
	return cnt_udpate

def generateSingleUrl(url):
	outlinks_str = getOutlinksString(url)
	if outlinks_str == 0:
		return 0;
	outlinks_arr = outlinks_str.split(',')
	proper_links = filterOutLinks(outlinks_arr)
	cnt_udpate = update(proper_links)
	print 'Generate - ' + url,
	print ' out_links:%s proper_links:%s update_links:%s'%(len(outlinks_arr)-1 , len(proper_links),cnt_udpate )
	return cnt_udpate

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
	cnt_udpate = 0
	for row in rows:
		url = row[1]
		cnt_udpate += generateSingleUrl(url)
		
	cursor.close()
	conn.close()
	print 'Generate - Summary : All:%s New:%s'%(numrows,cnt_udpate)
	return 1



