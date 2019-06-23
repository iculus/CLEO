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
	active = getActive()
	names = visible()
	return render_template('template.html', my_string=active, my_list=names, activities=names)


@app.route('/signup', methods = ['POST'])
def signup():
	pw = request.form['pw']
	wifi = request.form['wifi']

	cmd = 'echo admin | sudo -S python /home/admin/CLEO/Connect/connectionManager.py ' + str(wifi) + " " + str(pw)

	print cmd

	call(cmd, shell=True)
	print("The wifi is '" + wifi + "'" + " The password is '" + pw + "'")

	return redirect('/')		

if __name__ == '__main__':
	app.run()
