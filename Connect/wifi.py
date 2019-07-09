#wsgi is in /var/www/FlaskApp
#sudo service apache2 restart

import sys, subprocess

sys.path.insert(0,'/home/admin/CLEO/Installer/')

sys.path.insert(1,'/home/admin/CLEO/Connect/')
sys.path.insert(2,'/home/admin/CLEO/Utilities/')

from installer import getSetup
from subprocess import Popen, PIPE, call
from ssid import *
from connectionManager import *
from readTemps import getTemps

#name, number, ngrokhttp, ngroktcp, password, ip, wifipassword = getSetup()

path = '/home/admin/CLEO/'

def checkService():

	ngrok = False
	lights = False
	sensors = False
	leap = False
	ngrokweb = False

	pl = (subprocess.Popen(['ps', '-U', '0', 'aux'], stdout=subprocess.PIPE).communicate()[0]).split('\n')
	for index, j in enumerate(pl):
	
		if "read.py" in j and "python" in j: sensors = True
		if "lightMessage2.py" in j and "python" in j: lights = True
		if "ngrok" in j and "tcp" in j: ngrok = True
		if "ngrok" in j and "http" in j: ngrokweb = True
		if "leapController.py" in j and "python" in j: leap = True

	return sensors, lights, ngrok, ngrokweb, leap

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/")
def template_test():
	active = getActive()
	names = visible()
	temps = getTemps()
	sensors, lights, ngrok, ngrokweb, leap = checkService()
	return render_template('template.html', my_string=active, my_list=names, activities=names, temperatures=temps, sensor_bool = sensors, lights_bool = lights, ngrok_bool = ngrok, ngrokweb_bool = ngrokweb, leap_bool = leap)
	#return render_template('template.html', my_string=active, my_list=names, activities=names, temperatures=temps)


@app.route('/signup', methods = ['POST'])
def signup():
	pw = request.form['pw']
	wifi = request.form['wifi']


	#password
	password = 'crystalz'
	cmd = 'echo '+ password +' | sudo -S python /home/admin/CLEO/Connect/connectionManager.py -u ' + str(wifi) + " -p " + str(pw)

	print cmd

	call(cmd, shell=True)
	print("The wifi is '" + wifi + "'" + " The password is '" + pw + "'")

	return redirect('/')		

app.debug = True

if __name__ == '__main__':
	#remove before flight
	app.run()
