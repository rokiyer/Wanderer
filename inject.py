import database

conn = database.getConn()
cursor = conn.cursor()

total = 0
succ = 0
fail = 0

f = open("url.txt" , 'r')
for line in f.readlines():
	print line
	total += 1
	sql = "SELECT * FROM webpage WHERE url = %s"
	param = ( line )
	cursor.execute(sql,param)
	numrows = int(cursor.rowcount)
	if numrows == 0:
		sql = "INSERT INTO webpage SET url = %s"
		param = ( line )
		result = cursor.execute(sql,param)
		if result == 1:
			succ += 1
			continue

	fail += 1

cursor.close()
conn.close()
f.close()

print 'total:%d'%(total)
print 'succ:%d'%(succ)
print 'fail:%d'%(fail)


    