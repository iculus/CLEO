#!/usr/bin/env python

import sys, subprocess, time, datetime, os
sys.path.insert(0,'/home/admin/CLEO/Leap')
sys.path.insert(0,'/home/admin/CLEO')
sys.path.insert(0,'/home/admin/CLEO/Launcher')
from procCtl import set_procname
import pytz
from datetime import datetime

ngrokLaunches = 0
ngrokwebLaunches = 0
lightsLaunches = 0
sensorsLaunches = 0
leapLaunches = 0

path = "/home/admin/CLEO/"

thresh = 3
timeLast = time.time()

set_procname('crystalz-launcher')

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

while True:
	
	tz = pytz.timezone('US/Pacific')
	timeNow = time.time()
	currentDT = datetime.now(tz)

	#print ("Current Hour is: %d" % currentDT.hour)
	#print ("Current Minute is: %d" % currentDT.minute)
	#print ("Current Second is: %d" % currentDT.second)

	if currentDT.hour == 01 and currentDT.minute == 56 and currentDT.second == 00:
		os.system('sudo reboot')
		print "reboot"

	if timeNow-timeLast <= thresh:
		time.sleep(0.66)

	if timeNow-timeLast > thresh:

		print ("Current Hour is: %d" % currentDT.hour)
		print ("Current Minute is: %d" % currentDT.minute)
		print ("Current Second is: %d" % currentDT.second)
		
		timeLast = timeNow

		sensors, lights, ngrok, ngrokweb, leap = checkService()
			
		print '\n', timeNow			
		print "leap      : ", leap, "-",  leapLaunches
		print "lights    : ", lights, "-",  lightsLaunches
		print "sensors   : ", sensors, "-",  sensorsLaunches
		print "ngrok     : ", ngrok, "-",  ngrokLaunches
		print "ngrok web : ", ngrokweb, "-",  ngrokwebLaunches
		print '\n'

		ngrok = ngrokweb = True


		if not ngrok: 
			print "launching : NGROK"
			p = subprocess.Popen(["gnome-terminal", "-x", "sh", "-c", "'/home/admin/CLEO/Launcher/grok.sh'"], 					cwd=path, shell=False)
			p.wait()
			ngrokLaunches += 1
			print "NGROK running"

		if not ngrokweb: 
			print "launching : NGROK web"
			o = subprocess.Popen(["gnome-terminal", "-x", "sh", "-c", "'/home/admin/CLEO/Launcher/grokweb.sh'"], 					cwd=path, shell=False)
			o.wait()
			ngrokwebLaunches += 1
			print "NGROK web running"
		
		if not leap: 
			print "launching : LEAP"
			q = subprocess.Popen(["gnome-terminal", '-e', path + "Launcher/leap.sh"], 					shell=False)
			q.wait()
			leapLaunches += 1
			print "LEAP running"

		if not sensors: 
			print "launching : SENSORS"
			r = subprocess.Popen(["gnome-terminal", '-e', path + "Launcher/sensors.sh"], 					shell=False)
			r.wait()
			sensorsLaunches += 1
			print "SENSORS running"

		if not lights: 
			print "launching : LIGHTS"
			s = subprocess.Popen(["gnome-terminal", '-e', path + "Launcher/lights.sh"], 					shell=False)
			s.wait()
			lightsLaunches += 1
			print "LIGHTS running"

		sys.stdout.flush()
