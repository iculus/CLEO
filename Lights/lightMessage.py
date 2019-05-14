#!/usr/bin/python

import os, signal, sys, inspect, thread, time, random, struct
from numpy import interp, zeros, chararray, reshape, append, array, roll, fliplr, where, add

#sys.path.insert(0,'/home/admin/Desktop/cuttlefishLights/leapController/')
sys.path.insert(0,'/home/admin/CLEO/Leap/')
sys.path.insert(0,'/home/admin/CLEO/Setup/')
sys.path.insert(0,'/home/admin/CLEO/Sockets/')
sys.path.insert(1,'/usr/lib/python2.7')
import subprocess

from patterns import *
from setup import *
from SensorSetup import sendIt, setupSerial
from procCtl import setupProcess, set_procname

from sockets import *

if __name__ == "__main__":
	
	# setup area #
	ser = setupSerial(LEDComputer)
	ser2 = setupSerial(SENSORComputer)
	newSim = dot(1,1,35)
	simulator2 = chevronLine(False)
	simulator3 = diagonalLine()
	simulator4 = dot(5,9,4)
	simulator5 = heart(4)
	simulator6 = makeSaw(76)
	simulator7 = makeSaw(26)
	simulator8 = heart(83)

	count = 0
	maxCount = 22
	numFing = 0
	startTime = currentTime = lastTimeDelay = lastTimeMode = time.time()
	worked = True
	set_procname("crystalz-light")
	
	#mode setup
	delay = 0.0
	modeDelay = 12000
	maxMode = 18
	oneMode = False
	thisMode = 18
	mode = thisMode
	fade = False

	#states
	state = 0
	switch = 1
	state2 = 0
	bright = 0
	sign = 1

	#for fingers and demo chosing and ranging
	demo = True
	fingers = False
	justSawFingers = False
	decayTimeStart = time.time()
	ranger="4.4"
	volts="4.4"
	button="4.4"
	personNearby = False
	selector = 0

	#setupProcess("leapd", "sudo leapd &")

	#pusubsetup
	port = "5556"
	socketA = setupListenSocket(port,"10001")

	#setup Timers
	timeStart = time.time()

	#start threads
	lThreadA = startThreads(socketA, listenThread())

	#lThread = listenThread()
	#lThread.start()

	count = 0

	#people simulator
	distanceMin = 10
	distanceMax = 1200
	distanceErr = 8190
	distance = distanceMin
	distanceSign = 1
	reading = False
	timeoutCounter = 0
	person = False
	d = 0

	#events
	justEnteredDemo = False
	justEnteredFingers = False
	justEnteredPerson = False
	peopleEvents = 0
	fingerEvents = 0
	demoEvents = 0

	def map(x, in_min, in_max, out_min, out_max):
		return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

	#body of program
	while True:

		#print ranger

		#map ranger to steps
		rangerMin = 0
		rangerMax = 7

		if ranger > 8180 and ranger < 8200:
			reading = False

		elif ranger <= distanceMax:
			reading = True	
			timeoutCounter = 0	
			d = map(ranger, distanceMin, distanceMax, rangerMin, rangerMax)
		
		#check for people
		if d > 1 and d < 7 and reading == True:
			personNearby = True
		elif d <= 1 or d >= 7 and reading == True:
			personNearby = False
		elif reading == False:
			timeoutCounter = timeoutCounter + 1
			if timeoutCounter > 20:
				timeoutCounter = 0
				personNearby = False
		#if reading == True:
		#print reading, personNearby, ranger

		
		if reading and personNearby: 
			person = True
			demo = False
			#print "hi"
		
		if not reading and not personNearby:
			person = False
			demo = True
			#print "bye"

		#here we know if there is a person or not

		#update
		currentTime = time.time()

		
		#get fingers info			
		fingerUpdate = False
		fingerTopic = 0
		fingerPos = 0,0
		fingerNum = 0

		fingInfo = str(lThreadA).replace(" ", "")
		if fingInfo != "NONE": 
			fingerTopic, fingerPos, fingerNum = fingInfo.split(":")
			fingerPos = fingerPos.strip('[').strip(']').split('),(')

		if len(fingerPos) > 2:
			for index,fing in enumerate(fingerPos):
				x,y,z = fing.strip('(').strip(')').split(',')
				thisFing = (int(x), int(y), int(z))
				#print index,thisFing
				fingerPos[index] = thisFing
			fingerUpdate = True
			negOneCount = 0
			for f in fingerPos:
				for ff in f:
					if ff == -1:
						negOneCount = negOneCount + 1
			if negOneCount == 30:
				fingers = False

		fingerNum = int(fingerNum)
		
		#have finger info
		
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

		modes = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
		numModes = len(modes)

		#skipList = []
		skipList = [18,15,3]

		agro = [3,18]

		heart = [10,15]

		calm = [0,14,12.9]

		alien = [12,4]

		water = [6,1]		

		favList = [11,13,16,0,5,8,17]

		boring = [2]

		happy = False
		angry = False
		bored = False

		if happy: modes = favList+water+calm+heart
		if angry: modes = favList+agro+alien+water
		if bored: modes = water+alien
		
		#update mode
		modeDelay = 1
		if (currentTime - lastTimeMode) > modeDelay:
			if oneMode: mode = thisMode
			if not oneMode: mode += 1;
			if mode > maxMode: mode = 0
			lastTimeMode = currentTime
			selector = random.randrange(numModes)


		
		if selector not in skipList:
			mode = modes[selector]
		if selector in skipList:
			selector = random.randrange(len(favList))
			mode = favList[selector]
		
		
		#print modes, numModes, selector

#		mode = 5

		print mode

		def diags(xVal, yVal,color, newSim):
			for i,valI in enumerate(xVal):
				for j, valJ in enumerate(yVal):
					thisMatrix = dot(yVal[j],xVal[i],color)
					newSim = where(newSim != 0, newSim, thisMatrix)
			return newSim
		
		if (currentTime - lastTimeDelay) > delay:
			#if person nearby
			if not person: justEnteredPerson = True
			if person:
				if justEnteredPerson:
					peopleEvents = peopleEvents + 1
					justEnteredPerson = False
				fade = True
				newSim = dot(0,0,0)

				if d >= 1 and d > 0:
					xVal = [5]
					yVal = [11]
					color = 15
					thisMatrix = diags(xVal, yVal,color, newSim)
					newSim = where(newSim != 0, newSim, thisMatrix)
				
				if d >= 2 and d > 0:
					xVal = [4,6]
					yVal = [10,12]
					color = 25
					thisMatrix = diags(xVal, yVal,color, newSim)
					newSim = where(newSim != 0, newSim, thisMatrix)

				if d >= 3 and d > 0:
					xVal = [3,7]
					yVal = [9,13]
					color = 35
					thisMatrix = diags(xVal, yVal,color, newSim)
					newSim = where(newSim != 0, newSim, thisMatrix)

				if d >= 4 and d > 0:
					xVal = [2,8]
					yVal = [8,14]
					color = 45
					thisMatrix = diags(xVal, yVal,color, newSim)
					newSim = where(newSim != 0, newSim, thisMatrix)

				if d >= 5 and d > 0:
					xVal = [1,9]
					yVal = [7,15]
					color = 55
					thisMatrix = diags(xVal, yVal,color, newSim)
					newSim = where(newSim != 0, newSim, thisMatrix)

				if d >= 6 and d > 0:
					xVal = [0,10]
					yVal = [6,16]
					color = 65
					thisMatrix = diags(xVal, yVal,color, newSim)
					newSim = where(newSim != 0, newSim, thisMatrix)

				

				#print newSim

				#fade = False
			

			#if fingers are lost for a short time
			if justSawFingers == True:
				newSim = roll(newSim,-1,0)
				fade = True
				if currentTime-decayTimeStart > 10:
					justSawFingers = False
					fingers = False

			#if we are in a demo mode
			#print mode
			if not demo: justEnteredDemo = True
			if demo:
				if justEnteredDemo:
					demoEvents = demoEvents + 1
					justEnteredDemo = False
				#dichro
				if mode == 0: 
					newSim,count = patternZero(newSim,count)
					fade = True
					#delay = 1
				#2 chevrons purp blue
				if mode == 1: 
					newSim, simulator2 = patternOne(simulator2,86,66)
				#2 chevrons bl yl
				if mode == 2: newSim, simulator2 = patternTwo(simulator2,36,66)
				#2 chevrons alt fast red blue
				if mode == 3: newSim, simulator2 = patternThree(simulator2,15,65)
				#green stripe on blue
				if mode == 4: 
					newSim, simulator2,count = patternFour(simulator2,32,65,count)
					fade = False
				#yellow with blue chevron
				if mode == 5: 
					newSim, simulator2 = patternFive(simulator2,54,64,34,2)
					fade = False
				#very blue
				if mode == 6: newSim, simulator2 = patternSix(simulator2,33,66)
				#very purp
				if mode == 12: newSim, simulator2 = patternSix(simulator2,33,76)
				#blue red chevron
				if mode == 7: newSim, simulator2,count = patternFour(simulator2,24,65,count)
				#2 chevrons peach and purp
				if mode == 8: newSim, simulator2 = patternEight(simulator2,76,26)
				
				'''
				#pink waves
				if mode == 9: 
					newSim, state, switch = patternNine(state,34, switch)
				'''
				#pink waves				
				if mode == 13:newSim, simulator6, state2 = patternTen(simulator6,state2,44)
				#love 11 pink wiggles with heart
				if mode == 11:
					newSim, simulator6, state2 = patternTen(simulator6,state2,44)
					newSim =  where(simulator5!=0,simulator5,newSim)
				#yellow with heart				
				if mode == 18:
					newSim, state, switch = patternNine(state,34, switch)
					newSim =  where(simulator5!=0,simulator5,newSim)
				if mode == 10:
					newSim, simulator6, state2 = patternTen(simulator6,state2,44)
					newSim =  where(simulator5==0,simulator5,newSim)
				#specular 				
				if mode == 14:
					newSim,count = patternZero(newSim,count)
					fade = True
					#delay = 1
				if mode == 9:
					newSim,count = patternZero(newSim,count)
					fade = True
					#delay = 1
				#red heart				
				if mode == 15:
					fade = True
					newSim = simulator5
				#peach wiggle 
				if mode == 16:
					newSim, simulator7, state2 = patternTen(simulator7,state2,56)
					simulator8 = roll(simulator8,-1,0)
					newSim =  where(simulator8!=0,simulator8,newSim)
				#yellow with blue chevron
				if mode == 17: 
					newSim, simulator2 = patternFive(simulator2,56,66,14)
					fade = False

			lastTimeDelay = currentTime
		
			#if we see fingers 
			if not fingers: justEnteredFingers = True
			if fingers:
				if justEnteredFingers:
					fingerEvents = fingerEvents + 1
					justEnteredFingers = False
				fade = False
				delay = 0
				justSawFingers = True
				decayTimeStart = time.time()
				#print fingerPos
				newSim = dot(0,0,0)
				#print fingerNum	  
				for index, info in enumerate(fingerPos):
					color = (index*10) + 6
					if info[1] >= 0 and info[0] >= 0:
						if info[0] < 11 and info[1] < 22:
							#print info[0],info[1],color
							thisMatrix = dot(info[1],info[0],color)
							newSim = where(newSim != 0, newSim, thisMatrix)
				#print newSim, '\n'
				fingerNum = 5
				#newSim, state, switch = patternNine(state,color, switch)
				lastTimeDelay = currentTime

			
		#show
		if fade:
			step = 5
			if bright == 0: sign = 1; count = count+12; justSawFingers = False
			sendIt(newSim, fingerNum, ser, bright)
			bright = bright+(step*sign)
			if bright >= 255-step+1:
				sign = -1
		if not fade:
			sendIt(newSim, fingerNum, ser, 255)

	#end threads
	lThreadA.join()
