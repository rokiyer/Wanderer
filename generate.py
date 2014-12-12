import database
import re

def generateSingleUrl(url):
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE url = %s"
	param = (url)
	cursor.execute(sql,param)
	numrows = int(cursor.rowcount)
	if numrows == 0:
		print 'Url does not exist in webpage'
		return 0
	row = cursor.fetchone()
	generateOutlinks(row[10])
	cursor.close()
	conn.close()
	

#input : outlik_str is a list of outlinks separated by ','
#output : links number , matched number , inserted number
def generateOutlinks(outlink_str):
	conn = database.getConn()
	cursor = conn.cursor()
	outlinks = outlink_str.split(',')

	cnt_all = 0
	cnt_matched = 0
	cnt_inserted = 0

	for link in outlinks:
		#url must be sjtu.edu.cn
		print link,
		cnt_all += 1
		re_sjtu = re.compile('(^http://([a-z0-9]*\.)*sjtu.edu.cn(/)?)',re.I)
		result = re_sjtu.match(link)
		if result:
			print 'matched',
			cnt_matched += 1
			# check whether link in webpage
			sql = "SELECT * FROM webpage WHERE url = %s"
			param = (link)
			cursor.execute(sql,param)
			if cursor.rowcount == 0:
				#insert link into page 
				sql = "INSERT INTO webpage SET url = %s"
				param = (link)
				cursor.execute(sql,param)
				print 'inserted'
				cnt_inserted += 1
			else:
				print 'existed'
		else:
			print 'notMatch'

	print 'links:%d matched:%d inserted:%d'%(cnt_all,cnt_matched,cnt_inserted)
	cursor.close()
	conn.close()
	return (cnt_all,cnt_matched,cnt_inserted)

def generateAll():
	conn = database.getConn()
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE status = 2"
	cursor.execute(sql)
	numrows = int(cursor.rowcount)
	if(numrows == 0):
		print 'There is no parsed url waiting to be fetched'
		return 0
	rows = cursor.fetchall()
	for row in rows:
		url = row[1]
		outlinks_str = row[10]
		generateOutlinks(outlinks_str)
		sql = "UPDATE webpage SET status = 3 WHERE url = %s"
		param = (url)
		cursor.execute(sql , param)
	cursor.close()
	conn.close()
	print 'Summary'
	print 'Generate %d fetched url'%numrows

generateAll()