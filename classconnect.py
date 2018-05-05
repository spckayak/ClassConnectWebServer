from flask import *
import os, MySQLdb, sys

sys.path.append('/CICD')
import vars

app = Flask(__name__)
app.debug = True
app.secret_key = 'aBcEasyAsoNe23!'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/register.html")
def register():
    return render_template('register.html')

@app.route("/courses.html")
def courses():
    return render_template('courses.html')

@app.route("/task.html")
def task():
    return render_template('task.html')

@app.route("/attend.html")
def attend():
    return render_template('attend.html')

@app.route("/analys.html")
def analys():
    return render_template('analys.html')

@app.route("/inbox.html")
def inbox():
    return render_template('inbox.html')

@app.route("/manual.html")
def manual():
    return render_template('manual.html')

@app.route("/dashboardstudent.html")
def dashboardstudent():
    return render_template('dashboardstudent.html')

@app.route("/dashboard.html")
def dashboard():
    try:	
    	fname = session['fname']
    except:
	return render_template('login.html') #Direct user to login

    config = {
			'host':'a',
			'user':'b',
			'passwd':'c',
			'db':'StudentLogin'
    }
    config['host'] = vars.host
    config['user'] = vars.user
    config['passwd'] = vars.password	
    sid = session['sid']
    syntax = "SELECT cid FROM Class_Stu where sid = '%s'" % (sid) #Get List of all classes belonging to student
    db = MySQLdb.connect(**config)
    cur = db.cursor()
    cur.execute(syntax)
    result = cur.fetchall()
    db.close()
    classlist = " "
    for row in result:
		cid = row[0]
		syntax = "SELECT Name, Section, Semester, Year FROM Class where cid = '%s'" % (cid) #Get List of all classes belonging to student
		db = MySQLdb.connect(**config)
		cur = db.cursor()
		cur.execute(syntax)
		response = cur.fetchone()
		db.close()
		className = response[0]
		classSect = response[1]
		classSeme = response[2]
		classYear = response[3]
		insertBox = "<div class=\"col-md-3 col-sm-6 col-xs-12\"><div class=\"info-box-content\"><span class=\"info-box-text\"><a href=\"task.html\">%s</a></span><span class=\"info-box-number\">%s - %s %s</span></div>" % (className,classSect,classSeme,classYear)
		classlist = classlist + insertBox
    classlist=Markup(classlist)
    return render_template('dashboard.html', fname=fname, classlist=classlist)

@app.route("/loginVerify", methods=['POST'])
def loginSubmit():
	config = {
				'host':'a',
				'user':'b',
				'passwd':'c',
				'db':'StudentLogin'
	}
	config['host'] = vars.host
	config['user'] = vars.user
	config['passwd'] = vars.password
	usernameReq = request.form['username']
	passwordReq = request.form['password']
	
	if usernameReq == "" or passwordReq == "": #Make sure fields are not empty
		message = "Fields cannot be empty"
		return render_template('login.html', message=message)
	
	db = MySQLdb.connect(**config)
	cur = db.cursor()
	command = "SELECT Password FROM Student where Username = '%s'" % (usernameReq)
	cur.execute(command)
	result = cur.fetchone()
	db.close()
	
	if not result: #Account not found
		message = "Login Unsuccessful, please try again"
		return render_template('login.html', message=message)
	
	elif passwordReq != result[0]: #Account found, and the password does not match
		message = "Login Unsuccessful, please try again"
		return render_template('login.html', message=message)	
	
	elif passwordReq == result[0]: #Account found, and the password matched
		db = MySQLdb.connect(**config)
		cur = db.cursor()
		command = "SELECT sid,fname FROM Student where Username = '%s'" % (usernameReq)
		cur.execute(command)
		result = cur.fetchone()
		db.close()
		
		session['username'] = usernameReq
		session['sid'] = result[0]
		session['fname'] = result[1]
		return redirect(url_for('dashboard'))
	
	else:
		message = "Unexpected Error has occured"
		return render_template('login.html', message=message)		
		
@app.route("/accountCreate", methods=['POST'])
def accountCreate():	
	fname = request.form['fname']
	lname = request.form['lname']
	major = request.form['Major']
	email = request.form['Email']
	usernameReq = request.form['username']
	passwordReq = request.form['password']
	if fname == "" or lname == "" or major == "" or email == "" or usernameReq == "" or passwordReq == "": #Make sure fields are not empty
		message = "Fields cannot be empty"
		return render_template('register.html', message=message)
	
	syntax = "SELECT Email FROM Student where Email = '%s'" % (email) #Check if email already exists
	config = {
				'host':'a',
				'user':'b',
				'passwd':'c',
				'db':'StudentLogin'
	}
	config['host'] = vars.host
	config['user'] = vars.user
	config['passwd'] = vars.password	

	db = MySQLdb.connect(**config)
	cur = db.cursor()
	cur.execute(syntax)
	result = cur.fetchone()
	db.close()
	
	if not result: # Email does not exist. Procceed to check existing username
		syntax = "SELECT Username FROM Student where Username = '%s'" % (usernameReq) #Check if username already exists
		config = {
					'host':'a',
					'user':'b',
					'passwd':'c',
					'db':'StudentLogin'
		}
		config['host'] = vars.host
		config['user'] = vars.user
		config['passwd'] = vars.password	

		db = MySQLdb.connect(**config)
		cur = db.cursor()
		cur.execute(syntax)
		result = cur.fetchone()
		db.close()
		
		if result: #Username exists
			message = "Username is taken, please select a new username"
			return render_template('register.html', message=message)
			
		elif not result: #Username does not exists, proceed wih account creation
			#GET NEW SID, 
			
			syntax = "SELECT COUNT(*) FROM Student" #Get Row Count
			config = {
						'host':'a',
						'user':'b',
						'passwd':'c',
						'db':'StudentLogin'
			}
			config['host'] = vars.host
			config['user'] = vars.user
			config['passwd'] = vars.password	

			db = MySQLdb.connect(**config)
			cur = db.cursor()
			cur.execute(syntax)
			result = cur.fetchone()
			db.close()
			sid = int(result[0]) + 1
			
			syntax = "INSERT INTO Student (Sid, Fname, Lname, Major, Email, Username, Password) VALUES('%s','%s','%s','%s','%s','%s','%s')" % (sid,fname,lname,major,email,usernameReq,passwordReq) 
			config = {
						'host':'a',
						'user':'b',
						'passwd':'c',
						'db':'StudentLogin'
			}
			config['host'] = vars.host
			config['user'] = vars.user
			config['passwd'] = vars.password	

			db = MySQLdb.connect(**config)
			cur = db.cursor()
			try:
				cur.execute(syntax)
				db.commit()
				message = "Account Created!"
			except:
				message = "Unexpected Error"
			result = cur.fetchone()
			db.close()
			return render_template('register.html', message=message)
			
		else:
			message = "Unexpected error has occured in checking account creation parameters."
			return render_template('register.html', message=message)
			
	elif result[0]: #Email found, forgot username is needed
		message = "This email already exists in our system."
		return render_template('register.html', message=message)	
		
	else:	
		message = "Unexpected error has occured in checking existing email."
		return render_template('register.html', message=message)

@app.route('/gitwebhook', methods=['POST'])
def webhook():
	req_data = request.get_json()
	os.chdir("/CICD")
	os.system("./gitPull.sh")
	return("OK")

if __name__ == "__main__":
    app.secret_key = 'aBcEasyAsoNe23!'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.debug = True
    app.run()
