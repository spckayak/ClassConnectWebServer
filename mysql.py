import os, MySQLdb, vars

def loginSubmit():

	config = "user='%s',passwd='%s',host='%s', port='3306', db='StudentLogin'" % (vars.user, vars.password, vars.host)
	#username = request.form.get('username', None)
	#username = request.form.get('password', None)
	db = MySQLdb.connect(config)
	cursor = db.cursor()
	cursor.execute("SELECT VERSION()")
	data = cursor.fetchall()
	db.close()
	return (data)