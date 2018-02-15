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
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
for row in cursor.fetchall() :
    print row[0], " ", row[1]
db.close()
