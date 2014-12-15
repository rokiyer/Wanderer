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

def filterLink(link):
	allow_patterns = reg_tools.allowUrlFilter()
	deny_patterns = reg_tools.denyUrlFilter()

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
		return link
	else:
		return ''

def addNewUrl():

	conn = database.getConn()
	cursor = conn.cursor()

	# check if empty
	cursor.execute('SELECT outlinks FROM webpage WHERE status = 2')
	num_outlinks = cursor.rowcount
	rows_outlinks = cursor.fetchall()
	cursor.execute("SELECT error FROM webpage WHERE status = 11")
	num_redirect = cursor.rowcount
	rows_redirect = cursor.fetchall()
	
	num_all = num_redirect + num_outlinks
	if num_all == 0 :
		return {'exist':0 , 'insert':0 , 'all':0}
		cursor.close()
		conn.close()

	#bloom start ..input the urls into bloom
	import bitarray
	from pybloom import ScalableBloomFilter
	
	sql = "SELECT url FROM webpage WHERE 1"
	cursor.execute(sql)
	num_exist = cursor.rowcount
	rows = cursor.fetchall()

	sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
	for row in rows:
		sbf.add(row[0])
	#bloom end  sbf

	insert_arr = []
	num_insert = 0

	for row in rows_outlinks:
		outlinks_arr = row[0].split(',')
		proper_links = filterOutLinks(outlinks_arr)
		for link in proper_links:
			if link in sbf:
				pass
			else:
				num_insert += 1
				sbf.add(link)
				insert_arr.append((link,0))

	# for the redirect url
	cursor.execute("SELECT error FROM webpage WHERE status = 11")
	rows = cursor.fetchall()
	for row in rows_redirect:
		link = row[0]
		link = filterLink(link) 
		if link == '':
			continue

		if link in sbf:
			pass
		else:
			num_insert += 1
			sbf.add(link)
			insert_arr.append((link,0))
	
	sql = "INSERT INTO webpage (url,status)VALUE(%s,%s)"
	cursor.executemany(sql,insert_arr)

	cursor.execute("UPDATE webpage SET status = 3 WHERE status = 2 OR status = 11")

	cursor.close()
	conn.close()

	return {'exist':num_exist , 'insert':num_insert , 'all':num_all}


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



