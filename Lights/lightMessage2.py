#!/usr/bin/python

import os, signal, sys, inspect, thread, time, random, struct
from numpy import interp, zeros, chararray, reshape, append, array, roll, fliplr, where, add

#sys.path.insert(0,'/home/admin/Desktop/cuttlefishLights/leapController/')
sys.path.insert(0,'/home/admin/CLEO/Leap/')
sys.path.insert(0,'/home/admin/CLEO/Setup/')
sys.path.insert(0,'/home/admin/CLEO/Sockets/')
sys.path.insert(1,'/usr/lib/python2.7')
import subprocess

from setup import *
from SensorSetup import sendIt, setupSerial
from procCtl import setupProcess, set_procname

from sockets import *
from fingers import *
from sensors import *

if __name__ == "__main__":
	ser = setupSerial(LEDComputer)
	ser2 = setupSerial(SENSORComputer)

	#pusubsetup
	fingerPort = "5556"
	fingerSocket = setupListenSocket(fingerPort,"10001")
	sensePort = "5557"
	senseSocket = setupListenSocket(sensePort,"10001")

	#start threads
	fingerThread = startThreads(fingerSocket, listenThread())
	senseThread = startThreads(senseSocket, listenThread())

	while True:
		#update
		currentTime = time.time()

		'''
		sensors - 0.000185012817383
		fingers - 0.000125885009766
		'''

		fingerNum, fingerPos = getFings(fingerThread)
		#print fingerNum, time.time() - currentTime
		if time.time()-currentTime > 0.0015:
			print "fingers slow", time.time() - currentTime

		reading, personNearby, ranger, d = sensors(senseThread)
		#print reading, personNearby, ranger, d, time.time() - currentTime
		if time.time()-currentTime > 0.002:
			print "sensors slow", time.time() - currentTime

		'''
		if reading and personNearby: 
			person = True
			demo = False
			#print "hi"
		
		if not reading and not personNearby:
			person = False
			demo = True
			#print "bye"
		'''
		#here we know if there is a person or not

	
		'''
		0 0.000144004821777
		0 0.00014591217041
		0 0.00014591217041
		'''

		'''have finger info'''
		
		

		'''
		#print fingerNum
		if fingerNum == 0: 
			if not person: demo = True
		if fingerNum > 0 and not fingerUpdate:
			fingers = False
			if not person: demo = True			
		if fingerNum > 0 and fingerUpdate: 
			fingers = True
			if not person: demo = False
		if justSawFingers: demo = False

		denom = ((time.time()-startTime)/100)+1

		print demo, demoEvents, demoEvents/denom
		print fingers, justSawFingers, fingerEvents, fingerEvents/denom
		print person, peopleEvents, peopleEvents/denom
		'''



	#end threads
	fingerThread.join()
	senseThread.join()
