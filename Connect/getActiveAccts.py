import sys, subprocess
sys.path.insert(0,'/home/admin/CLEO/Connect/')
sys.path.insert(0,'/home/admin/CLEO/Utilities')

from ssid import *
from connectionManager import *
from readTemps import getTemps


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

if __name__ == "__main__":
	print getActive()
	print visible()
	print getTemps()
	print checkService()
