from flask import Flask, render_template, request
import os, MySQLdb, vars
app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/logins.html")
def logins():
    return render_template('logins.html')

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

@app.route("/loginSubmit", methods=['POST'])
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

	usernameReq = request.form.get('username', None)
	passwordReq = request.form.get('password', None)
	db = MySQLdb.connect(**config)
	cur = db.cursor()
	command = "SELECT * FROM Student where Username = %s AND Password = %s" % (usernameReq, passwordReq)
	cur.execute(command)
	db.close()
	if not cur.rowcount: #If an entry was not matched
		return("Wrong Username or Password. Please try again")
	elif cur.rowcount:
		return 


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
