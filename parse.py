import database
import reg_tools

def parseSinglePage(url):
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

	if result == 1 :
		print "Succ:" + "Parse " + url
	else:
		print "Fail:" + "Parse " + url 

parsePage('http://www.sjtu.edu.cn')