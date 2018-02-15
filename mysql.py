import os, MySQLdb, vars

#config = "user='%s',passwd='%s',host='%s', port='3306', db='StudentLogin'" % (vars.user, vars.password, vars.host)
#username = request.form.get('username', None)
#username = request.form.get('password', None)
db = MySQLdb.connect(host = %s,
					user= %s,
					passwd= %s,
					db="StudentLogin" % (vars.host, vars.user, vars.password))
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
for row in cursor.fetchall() :
    print row[0], " ", row[1]
db.close()
