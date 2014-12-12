import database

def showInfo():
	conn = database.getConn()
	cursor = conn.cursor()

	sql = 'SELECT * FROM webpage WHERE status = 0'
	res = cursor.execute(sql)
	numrows = cursor.rowcount
	print 'unfetched : %s'%(numrows)

	sql = 'SELECT * FROM webpage WHERE status = 1'
	res = cursor.execute(sql)
	numrows = cursor.rowcount
	print 'fetched/unparsed : %s'%(numrows)

	sql = 'SELECT * FROM webpage WHERE status = 2'
	res = cursor.execute(sql)
	numrows = cursor.rowcount
	print 'parsed/ungenerated : %s'%(numrows)

	sql = 'SELECT * FROM webpage WHERE status = 3'
	res = cursor.execute(sql)
	numrows = cursor.rowcount
	print 'generated : %s'%(numrows)

	cursor.close()
	conn.close()

showInfo()