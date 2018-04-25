from flask import *
import os, MySQLdb, sys

sys.path.append('/CICD')
import vars

app = Flask(__name__)
app.debug = True

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
    return render_template('dashboard.html')

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
		return redirect(url_for('index'))
	
	else:
		message = "Unexpected Error has occured"
		return render_template('login.html', message=message)		
		
@app.route("/accountCreate", methods=['POST'])
def accountCreate():
	def mysqlCall(command):
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
		cur.execute(command)
		result = cur.fetchone()
		db.close()
		return result
	
	
	fname = request.form['fname']
	lname = request.form['lname']
	major = request.form['Major']
	email = request.form['Email']
	usernameReq = request.form['username']
	passwordReq = request.form['password']
	
	if fname == "" or lname == "" or major == "", or email == "" or usernameReq == "" or passwordReq == "" #Make sure fields are not empty
		message = "Fields cannot be empty"
		return render_template('register.html', message=message)
	
	request = "SELECT Email FROM Student where Email = '%s'" % (email) #Check if email already exists
	result = mysqlCall(request)
	
	if not result: # Email does not exist. Procceed to check existing username
		request = "SELECT Username FROM Student where Username = '%s'" % (usernameReq) #Check if username already exists
		result = mysqlCall(request)
		
		if result: #Username exists
			message = "Username is taken, please select a new username"
			return render_template('register.html', message=message)
			
		elif not result: #Username does not exists, proceed wih account creation
			#GET NEW SID, 
			
			request = "SELECT COUNT(*) FROM Student" #Get Row Count
			result = mysqlCall(request)
			sid = int(result[0]) + 1
			
			request = "INSERT INTO Student (Sid, Fname, Lname, Major, Email, Username, Password) VALUES('%s','%s','%s','%s','%s','%s','%s')" % (sid,fname,lname,major,email,usernameReq,passwordReq) 
			result = mysqlCall(request)
			
			message = "Account Created!"
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
	
@app.route('/trigger', methods=['POST']) #For Jenkins webhook
def trigger():
	if (request.data): #If a json object was recieved
		req_data = request.get_json()
		try:
			apitoken = req_data['apitoken']
			repo = req_data['repo']
			branch = req_data['branch']
		except:
			return("Post request recieved, but not all parameters were provided")

		if (apitoken) and (repo)and (branch):
			pullCmd="git clone https://08da1b41be17100cdad1948276feb081a2d1aabd@github.com/spckayak/ClassConnectWebServer.git"
			os.system("cd /home/ubuntu")
			os.system(pullCmd)
			return("Post Request Succesfull")
	else:
		return("Json Object was not recieved")

@app.route('/gitwebhook', methods=['POST'])
def webhook():
	req_data = request.get_json()
	os.chdir("/CICD")
	os.system("./gitPull.sh")
	return("OK")
