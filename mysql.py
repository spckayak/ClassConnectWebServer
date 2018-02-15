import os, MySQLdb, vars

config = "host='%s', user='%s', passwd='%s', port='3306', db='StudentLogin'" % (vars.host, vars.user, vars.password)
#username = request.form.get('username', None)
#username = request.form.get('password', None)
db = MySQLdb.connect(config)
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
for row in cursor.fetchall() :
    print row[0], " ", row[1]
db.close()
