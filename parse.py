import database
import reg_tools

def parseSinglePage(url):
	if reg_tools.allowUrl(url) == False:
		return 0

	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE url = %s"
	param = (url)
	cursor.execute(sql,param)
	numrows = int(cursor.rowcount)
	if(numrows == 0):
		return 0
	row = cursor.fetchone()
	content = row[4]
	head = row[3]
	# find out urls
	title = reg_tools.findTitle(content)
	outlinks = reg_tools.findUrls(content)
	text = reg_tools.filter_tags(content)
	last_modify_time = reg_tools.findLastModifyTime(head)

	sql = "UPDATE webpage SET status=2,title=%s,text=%s,outlinks=%s,modified_time=%s WHERE url=%s"
	param = (title,text,outlinks,last_modify_time,url)
	result = cursor.execute(sql,param)
	cursor.close()
	conn.close()
	return result

	
def parseAll():
	print 'Start parse all fetched url ...'
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE status = 1"
	cursor.execute(sql)
	numrows = cursor.rowcount
	if(numrows == 0):
		print 'Summary : There is no url waiting to parse'
		return 0
	else:
		cnt_succ = 0;
		rows = cursor.fetchall()
		for row in rows:
			url = row[1]
			result = parseSinglePage(url)
			if result == 1 :
				print "Succ:" + "Parse " + url
			else:
				print "Fail:" + "Parse " + url 
		print 'Summary : All:%s Succ:%s Fail:%s'%(numrows , cnt_succ , numrows - cnt_succ)


parseAll()