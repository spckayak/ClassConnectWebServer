import os, vars
import MySQLdb
config = {
	'host':'a',
	'user':'b',
	'passwd':'c', 
	'db':'StudentLogin' 
}
config['host'] = vars.host
config['user'] = vars.user
config['passwd'] = vars.password

#username = request.form.get('username', None)
#username = request.form.get('password', None)
db = MySQLdb.connect(**config)
cur = db.cursor()
cur.execute("DESCRIBE Student")
for row in cur.fetchall() :
    print row[0]
db.close()
