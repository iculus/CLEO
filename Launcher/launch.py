#!/usr/bin/env python

import sys, subprocess, time
sys.path.insert(0,'/home/admin/CLEO/Leap')
sys.path.insert(0,'/home/admin/CLEO')
sys.path.insert(0,'/home/admin/CLEO/Launcher')
from procCtl import set_procname

ngrok = False
lights = False
sensors = False
leap = False

ngrokLaunches = 0
lightsLaunches = 0
sensorsLaunches = 0
leapLaunches = 0

path = "/home/admin/CLEO/"

thresh = 3
timeLast = time.time()

set_procname('crystalz-launcher')

while True:
	
	timeNow = time.time()

	if timeNow-timeLast <= thresh:
		time.sleep(0.66)

	if timeNow-timeLast > thresh:
		
		timeLast = timeNow
	
		ngrok = False
		lights = False
		sensors = False
		leap = False

		pl = (subprocess.Popen(['ps', '-U', '0', 'aux'], stdout=subprocess.PIPE).communicate()[0]).split('\n')
		for index, j in enumerate(pl):
			if "read.py" in j: sensors = True
			if "lightMessage2.py" in j: lights = True
			if "ngrok" in j: ngrok = True
			if "leapController.py" in j: leap = True
			if index == 0 : print "Read Top"


		print '\n', timeNow			
		print "leap    : ", leap, "-",  leapLaunches
		print "lights  : ", lights, "-",  lightsLaunches
		print "sensors : ", sensors, "-",  sensorsLaunches
		print "ngrok   : ", ngrok, "-",  ngrokLaunches
		print '\n'


		if not ngrok: 
			print "launching : NGROK"
			p = subprocess.Popen(["gnome-terminal", "-x", "sh", "-c", "'/home/admin/CLEO/Launcher/grok.sh'"], 					cwd=path, shell=False)
			p.wait()
			ngrokLaunches += 1
			print "NGROK running"
		
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
