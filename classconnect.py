from flask import Flask, render_template, request
import os, mysql.connector, vars
app = Flask(__name__)
app.debug = True

config =  {'user':'','password':'','host':'','database':'StudentLogin'}
config['user']=vars.user
config['password']=vars.password
config['host']=vars.host

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/logins.html")
def login():
    return render_template('logins.html')

@app.route("/dashboard.html")
def dashboard():
    return render_template('dashboard.html')

@app.route("/loginSubmit")
def loginSubmit():
	try:
		connection = mysql.connector.connect(config)
		cursor = connection.cursor()
		loginSubmit = (cursor.execute("SHOW TABLES"))
		
		##loginInfo = request.form['projectPath']
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
    			return(err)
  	connection.close()
	return (loginSubmit)

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
