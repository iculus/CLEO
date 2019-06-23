#wsgi is in /var/www/FlaskApp
#sudo service apache2 restart

import sys
sys.path.insert(0,'/home/admin/CLEO/Connect/')
#sys.stdout = open('/home/admin/CLEO/Connect/output.logs', 'w')
from subprocess import Popen, PIPE, call
from ssid import *
from connectionManager import *
path = '/home/admin/CLEO/'

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/")
def template_test():
	names = visible()
	#print ("mike")
	return render_template('template.html', my_string="Heyo", my_list=names, activities=names)


@app.route('/signup', methods = ['POST'])
def signup():
	pw = request.form['pw']
	wifi = request.form['wifi']
	#connectNow(wifi,pw)
	#echo admin | sudo -S python connectionManager.py lupa buttaire

	#subprocess.Popen(['echo','admin','|','sudo','-S','python','/home/admin/CLEO/Connect/connectionManager.py','Mars','frozenbread'], shell=True)

	#sudo_password = 'admin'
	#command = ('python connectionManager.py ' + str(wifi) + ' ' + str(pw))
	#command = str(command).split()

	#command = ('python connectionManager.py Mars frozenbread').split()
	
	#call(["gnome-terminal", '-e', path + "Connect/openTerminal.sh"])

	#cmd = ["gnome-terminal", '-e', path + "Connect/openTerminal.sh"]

	#print cmd

	#p = subprocess.Popen(cmd, 
	#	stdout=subprocess.PIPE,
	#	stderr=subprocess.PIPE,
	#	stdin=subprocess.PIPE)
	#out,err = p.communicate()

	cmd2 = 'bash '+path+'Connect/openTerminal.sh ' + str(wifi) + " " + str(pw)

	cmd = 'echo admin | sudo -S python /home/admin/CLEO/Connect/connectionManager.py ' + str(wifi) + " " + str(pw)

	print cmd
	#cmd = str(cmd).split()
	print cmd

	call(cmd, shell=True)
	print("The wifi is '" + wifi + "'" + " The password is '" + pw + "'")

	return redirect('/')		

	#print command
	
	#p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
	#sudo_prompt = p.communicate(sudo_password + '\n')[1]

	


	#return redirect('/')


if __name__ == '__main__':
	app.run()
