from flask import Flask, render_template, request
import os
app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')

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
