import database
import re
import reg_tools

def getOutlinksString(url):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE url = '%s'"%(url)
	cursor.execute(sql)
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

def addNewUrl():

	conn = database.getConn()
	cursor = conn.cursor()

	# check if empty
	cursor.execute('SELECT outlinks FROM webpage WHERE status = 2')
	all_num = cursor.rowcount
	if all_num == 0:
		return {'exist':0 , 'insert':0 , 'all':0}
		cursor.close()
		conn.close()

	#bloom start ..input the urls into bloom
	import bitarray
	from pybloom import ScalableBloomFilter
	
	sql = "SELECT url FROM webpage WHERE 1"
	cursor.execute(sql)
	exist_num = cursor.rowcount
	rows = cursor.fetchall()

	sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
	for row in rows:
		sbf.add(row[0])
	#bloom end  sbf
	cursor.execute('SELECT outlinks FROM webpage WHERE status = 2')
	rows = cursor.fetchall()

	insert_arr = []
	insert_num = 0
	for row in rows:
		outlinks_arr = row[0].split(',')
		proper_links = filterOutLinks(outlinks_arr)
		for link in proper_links:
			if link in sbf:
				pass
			else:
				insert_num += 1
				sbf.add(link)
				insert_arr.append((link,0))

	# for the redirect url
	cursor.execute("SELECT error FROM webpage WHERE status = 11")
	rows = cursor.fetchall()
	for row in rows:
		link = row[0]
		if link in sbf:
			pass
		else:
			insert_num += 1
			sbf.add(link)
			insert_arr.append((link,0))
	
	sql = "INSERT INTO webpage (url,status)VALUE(%s,%s)"
	cursor.executemany(sql,insert_arr)

	cursor.execute("UPDATE webpage SET status = 3 WHERE status = 2 OR status = 11")

	cursor.close()
	conn.close()

	return {'exist':exist_num , 'insert':insert_num , 'all':all_num}


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

def generateAll():
	print 'Generate - start to generate all parsed urls'
	result = addNewUrl()
	print 'Generate - Summary : all %s exist %s insert %s'%(result['all'] , result['exist'] , result['insert'])
	return 1



