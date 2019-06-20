#!/usr/bin/env python

import sys, subprocess, time
sys.path.insert(0,'/home/admin/CLEO/Leap')
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

thresh = 1
timeLast = time.time()

if __name__ == "__main__":
	set_procname('crystalz-launcher')

	while True:
		
		timeNow = time.time()

		if timeNow-timeLast > thresh:
			
			timeLast = timeNow
		
			ngrok = False
			lights = False
			sensors = False
			leap = False

			pl = (subprocess.Popen(['ps', '-U', '0', 'aux'], stdout=subprocess.PIPE).communicate()[0]).split('\n')
			for j in pl:
				if "read.py" in j: sensors = True
				if "lightMessage2.py" in j: lights = True
				if "ngrok" in j: ngrok = True
				if "leapController.py" in j: leap = True

			print '\n', timeNow			
			print "leap    : ", leap, "-",  leapLaunches
			print "lights  : ", lights, "-",  lightsLaunches
			print "sensors : ", sensors, "-",  sensorsLaunches
			print "ngrok   : ", ngrok, "-",  ngrokLaunches
			print '\n'

			if not ngrok: 
				print "launching : NGROK"
				subprocess.call(["gnome-terminal", '-e', path + "Launcher/ngrok.sh"])
				ngrokLaunches += 1
				print "NGROK running"
			
			if not leap: 
				print "launching : LEAP"
				subprocess.call(["gnome-terminal", '-e', path + "Launcher/leap.sh"])
				leapLaunches += 1
				print "LEAP running"

			if not sensors: 
				print "launching : SENSORS"
				subprocess.call(["gnome-terminal", '-e', path + "Launcher/sensors.sh"])
				sensorsLaunches += 1
				print "SENSORS running"

			if not lights: 
				print "launching : LIGHTS"
				subprocess.call(["gnome-terminal", '-e', path + "Launcher/lights.sh"])
				lightsLaunches += 1
				print "LIGHTS running"
