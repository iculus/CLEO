#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess

start = chr(255)
end = chr(254)

def startProcess():
	p = subprocess.Popen(['./findDevicePath.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="/home/admin/CLEO/Utilities")
	out, err = p.communicate()
	return out

def checkLSUSB():
	p = subprocess.Popen(['lsusb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	return out

if __name__ == "__main__":

	FEATHERLOC = "X"
	LEONARDOLOC = "X"
	HUBLOC = "X"
	LEAPLOC = "X"
	WIFILOC = "X"

	tests = [FEATHERLOC,LEONARDOLOC,HUBLOC,LEAPLOC,WIFILOC]

	feather = "Adafruit_Feather_M4"
	leonardo = "Arduino_Leonardo"
	hub = "Realtek Semiconductor Corp. RTL"
	leap = "Leap Motion"
	wifi = "Ralink"

	testNames = [feather,leonardo,hub,leap,wifi]

	print "\nDevices\n"
	result = startProcess().split('\n')
	for res in result:
		try:
			dev,name = res.split(' - ')
			if "tty" in res:
				print dev,name 
				if feather in name:
					tests[0] = dev
				if leonardo in name:
					tests[1] = dev
			else:
				#print '\t',dev,name
				pass 	
		except:
			pass

	lsusb = checkLSUSB().split('\n')

	for thisUSB in lsusb:

		if leap in thisUSB:		
			print "LEAP - ", thisUSB
			tests[2] = thisUSB
		if hub in thisUSB:
			print "Hub  - ", thisUSB
			tests[3] = thisUSB
		if wifi in thisUSB:
			print "WIFI - ", thisUSB
			tests[4] = thisUSB

	print '\nResults\n'

	PASS = True

	for index, test in enumerate (tests):
		print "test ", index, "of ", len(tests) -1
		if test != "X":
			print testNames[index], ": OKAY"
		if test == "X":
			print testNames[index], ": ERROR"
			PASS = False

	print '\n'


	if len(testNames) != len(tests):
		print "program error, name Length mismatch"

	if PASS:
		print "passes tests\n"
	if not PASS:
		print "errors\n"
