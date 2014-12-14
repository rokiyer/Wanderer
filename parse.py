#!C:\Python27\python
# -*- coding: utf-8 -*-  
import database
import reg_tools
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   


def parse(url):
	if reg_tools.allowUrl(url) == False:
		return 0

	row = getRow(url)
	if row == None:
		return 0

	head = row[3]
	content = row[4]
	prev_modified_time = row[11]

	title = reg_tools.findTitle(content)
	text = reg_tools.filter_tags(content)
	outlinks = reg_tools.findUrls(content , url)
	last_modify_time = reg_tools.findLastModifyTime(head)

	return {'title':title,'outlinks':outlinks,'text':text,'last_modify_time':last_modify_time,'prev_modified_time':prev_modified_time}

def update(url,parse_result):
	if parse_result == 0:
		title = ''
		text = ''
		outlinks = ''
		prev_modified_time = 0
		last_modify_time = 0
		status = 20
	else:
		title = parse_result['title']
		text = parse_result['text']
		outlinks = parse_result['outlinks']
		prev_modified_time = parse_result['prev_modified_time']
		last_modify_time = parse_result['last_modify_time']
		status = 2

	conn = database.getConn()
	cursor = conn.cursor()
	sql = "UPDATE `webpage` SET `status`=%s,`title`=%s,`text`=%s,`outlinks`=%s,\
		`prev_modified_time`=%s,`modified_time`=%s WHERE `url`=%s"
	param = (status,title,text,outlinks,prev_modified_time,last_modify_time,url)
	try:
		cursor.execute(sql,param)
		result = 1
	except:
		result = 0
	cursor.close()
	conn.close()
	return result

def getContent(url):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE url = '%s'"%(url)
	cursor.execute(sql)
	row = cursor.fetchone()
	if row == None:
		return 0
	else:
		return row[4]

def getHead(url):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE url = '%s'"%(url)
	cursor.execute(sql)
	row = cursor.fetchone()
	if row == None:
		return 0
	else:
		return row[3]

def getRow(url):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE url = '%s'"%(url)
	cursor.execute(sql)
	row = cursor.fetchone()
	cursor.close()
	conn.close()
	return row
	
def parseAll(total = 100):
	print 'Parse - Start... %s url'%(total)
	if total == 'all':
		sql = "SELECT url FROM webpage WHERE status = 1"
	else:
		sql = "SELECT url FROM webpage WHERE status = 1 LIMIT %s"%(total)

	conn = database.getConn()
	cursor = conn.cursor()
	cursor.execute(sql)
	numrows = cursor.rowcount
	if(numrows == 0):
		print 'Parse - Summary : All:0 Succ:0 Fail:0'
		return 0
	else:
		cnt_succ = 0;
		rows = cursor.fetchall()
		for row in rows:
			url = row[0]
			print 'Parse - '+url,
			parse_result = parse(url)
			update(url,parse_result)
			if parse_result == 0 :
				print 'parse fail'
			else:
				cnt_succ += 1
				print 'parse succ'
		print 'Parse - Summary : All:%s Succ:%s Fail:%s'%(numrows , cnt_succ , numrows - cnt_succ)
		return 1

