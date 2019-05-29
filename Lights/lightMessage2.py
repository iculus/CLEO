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
#from patterns import *

if __name__ == "__main__":
	ser = setupSerial(LEDComputer, 500000, 0)

	#pusubsetup
	fingerPort = "5556"
	fingerSocket = setupListenSocket(fingerPort,"10001")
	sensePort = "5557"
	senseSocket = setupListenSocket(sensePort,"10001")

	#start threads
	fingerThread = startThreads(fingerSocket, listenThread())
	senseThread = startThreads(senseSocket, listenThread())

	#timers
	startTime = currentTime = lastTimeDelay = lastTimeMode = decayTimeStart = time.time()
	delaySave = 0.05

	#for the switches
	person = False
	demo = True
	fingers = False
	justSawFingers = False
	toc = 0

	#for the send
	bright = 0
	fade = True

	#for simulators
	sendSim = dot(0,0,0)
	simulator2 = chevronLine(True)

	#events
	justEnteredDemo = False
	demoEvents = 0
	justEnteredFingers = False
	fingerEvents = 0
	justEnteredPerson = False
	peopleEvents = 0

	while True:
		#update
		currentTime = time.time()

		fingerNum, fingerPos, fingerUpdate, fingers = getFings(fingerThread, fingers)
		if time.time()-currentTime > 0.0015:
			print "fingers slow", time.time() - currentTime

		reading, personNearby, ranger, d, toc = sensors(senseThread, toc)
		if time.time()-currentTime > 0.002:
			print "sensors slow", time.time() - currentTime

		
		'''sensors demo/person switch'''
		if reading and personNearby: 
			person = True
			demo = False
			#print "hi"
		
		if not reading and not personNearby:
			person = False
			demo = True
			#print "bye"

		
		'''fingers demo/person switch'''
		if fingerNum == 0: 
			if not person: demo = True
		if fingerNum > 0 and not fingerUpdate:
			fingers = False
			if not person: demo = True			
		if fingerNum > 0 and fingerUpdate: 
			fingers = True
			if not person: demo = False
		if justSawFingers: demo = False

		'''priorities'''
		if demo and person: demo = False
		if demo and fingers: demo = False
		if person and fingers: person = False
		if demo and fingers and person: person = False

		print demo, person, fingers
		demo = True

		'''
		denom = ((time.time()-startTime)/100)+1

		print demo, demoEvents, demoEvents/denom
		print fingers, justSawFingers, fingerEvents, fingerEvents/denom
		print person, peopleEvents, peopleEvents/denom
		'''

		def diags(xVal, yVal,color, newSim):
			for i,valI in enumerate(xVal):
				for j, valJ in enumerate(yVal):
					thisMatrix = dot(yVal[j],xVal[i],color)
					newSim = where(newSim != 0, newSim, thisMatrix)
			return newSim
		
		delay = delaySave
		if (currentTime - lastTimeDelay) > delay:
			lastTimeDelay = currentTime

			'''if person nearby'''
			if not person: justEnteredPerson = True
			if person:
				if justEnteredPerson:
					peopleEvents = peopleEvents + 1
					justEnteredPerson = False
				fade = True
				sendSim = dot(0,0,0)

				if d >= 1 and d > 0:
					xVal = [5]
					yVal = [11]
					color = 15
					thisMatrix = diags(xVal, yVal,color, sendSim)
					sendSim = where(sendSim != 0, sendSim, thisMatrix)
				
				if d >= 2 and d > 0:
					xVal = [4,6]
					yVal = [10,12]
					color = 25
					thisMatrix = diags(xVal, yVal,color, sendSim)
					sendSim = where(sendSim != 0, sendSim, thisMatrix)

				if d >= 3 and d > 0:
					xVal = [3,7]
					yVal = [9,13]
					color = 35
					thisMatrix = diags(xVal, yVal,color, sendSim)
					sendSim = where(sendSim != 0, sendSim, thisMatrix)

				if d >= 4 and d > 0:
					xVal = [2,8]
					yVal = [8,14]
					color = 45
					thisMatrix = diags(xVal, yVal,color, sendSim)
					sendSim = where(sendSim != 0, sendSim, thisMatrix)

				if d >= 5 and d > 0:
					xVal = [1,9]
					yVal = [7,15]
					color = 55
					thisMatrix = diags(xVal, yVal,color, sendSim)
					sendSim = where(sendSim != 0, sendSim, thisMatrix)

				if d >= 6 and d > 0:
					xVal = [0,10]
					yVal = [6,16]
					color = 65
					thisMatrix = diags(xVal, yVal,color, sendSim)
					sendSim = where(sendSim != 0, sendSim, thisMatrix)

			'''enter demo mode'''
			mode = 5
			if not demo: justEnteredDemo = True
			if demo:
				delay = delaySave
				if justEnteredDemo:
					demoEvents = demoEvents + 1
					justEnteredDemo = False

				#yellow with blue chevron
				if mode == 5: 
					sendSim, simulator2 = patternFive(simulator2,54,64,34,2)
					fade = True

			'''enter fingers mode'''
			if not fingers: justEnteredFingers = True
			if fingers:
				delay = 0
				if justEnteredFingers:
					fingerEvents = fingerEvents + 1
					justEnteredFingers = False
				fade = False
				justSawFingers = True
				decayTimeStart = time.time()
				sendSim = dot(0,0,0)	  
				for index, info in enumerate(fingerPos):
					color = (index*10) + 6
					if info[1] >= 0 and info[0] >= 0:
						if info[0] < 11 and info[1] < 22:
							thisMatrix = dot(info[1],info[0],color)
							sendSim = where(sendSim != 0, sendSim, thisMatrix)
				fingerNum = 5

			#if fingers are lost for a short time
			if justSawFingers == True:
				delay = delaySave
				sendSim = roll(sendSim,-1,0)
				fade = True
				if currentTime-decayTimeStart > 10:
					justSawFingers = False
					fingers = False


		#show
		if fade:
			step = 0.5
			if bright == 0: sign = 1; justSawFingers = False; #count = count+12; 
			sendIt(sendSim, fingerNum, ser, bright)
			bright = bright+(step*sign)
			if bright >= 255-step+1:
				sign = -1
		if not fade:
			sendIt(sendSim, fingerNum, ser, 255)

	#end threads
	fingerThread.join()
	senseThread.join()
