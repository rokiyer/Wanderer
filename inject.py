import database

conn = database.getConn()

total = 0
succ = 0
fail = 0

f = open("url.txt" , 'r')
for line in f.readlines():
	print line
	total += 1
	cursor = conn.cursor()
	sql = "SELECT * FROM webpage WHERE url = %s"
	param = ( line )
	cursor.execute(sql,param)
	numrows = int(cursor.rowcount)
	if numrows == 0:
		sql = "INSERT INTO webpage SET url = %s"
		param = ( line )
		cursor.execute(sql,param)
		succ += 1
	else:
		fail += 1

conn.close()
f.close()

print 'total:%d'%(total)
print 'succ:%d'%(succ)
print 'fail:%d'%(fail)


    