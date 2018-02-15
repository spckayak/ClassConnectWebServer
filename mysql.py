import os, vars
import MySQLdb
config = {
	'host':'a',
	'user':'b',
	'password':'c', 
	'database':'StudentLogin' 
}
config['host'] = vars.host
config['user'] = vars.user
config['password'] = vars.password

print config['host']
print config['user']
print config['password']
#username = request.form.get('username', None)
#username = request.form.get('password', None)
db = MySQLdb.connect(**config)
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
for row in cursor.fetchall() :
    print row[0], " ", row[1]
db.close()
