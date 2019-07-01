#!/usr/bin/python

import os, signal, sys, inspect, thread, time, random, struct
from numpy import interp, zeros, chararray, reshape, append, array, roll, fliplr, where, add, flipud

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
from patterns import *

if __name__ == "__main__":
	set_procname("crystalz-lights")
	ser = setupSerial(LEDComputer, 500000, 0)

	#pusubsetup
	fingerPort = "5556"
	fingerSocket = setupListenSocket(fingerPort,"10001")
	sensePort = "5557"
	senseSocket = setupListenSocket(sensePort,"10001")

	#start threads
	fingerThread = startThreads(fingerSocket, listenThread())
	senseThread = startThreads(senseSocket, listenThread())
	#fingerThread.daemon = False
	#senseThread.daemon = False

	#timers
	startTime = currentTime = lastTimeDelay = lastTimeMode = decayTimeStart = time.time()
	delaySave = 0.1
	personDelay = 0.08
	demoDelay = 0.07
	wanderDelay = 0.2
	fingerDelay = 0

	#for the switches
	person = False
	demo = True
	fingers = False
	justSawFingers = False
	toc = 0
	button = 0

	#modes
	selector = 0
	oneMode = False
	thisMode = 0
	modeDelay = 1200
	maxMode = 20
	mode = thisMode

	#copy of old modes setup
	count = 0
	maxCount = 22
	state = 0
	state2 = 0
	switch = 1
	newSim = dot(1,1,35)
	simulator2 = chevronLine(False)
	simulator3 = diagonalLine()
	simulator4 = dot(5,9,4)
	simulator5 = heart(4)
	simulator6 = makeSaw(76)
	simulator7 = makeSaw(26)
	simulator8 = heart(83)

	#for the send
	bright = 0
	fade = True

	#for simulators
	sendSim = dot(0,0,0)

	#events
	justEnteredDemo = False
	demoEvents = 0
	justEnteredFingers = False
	fingerEvents = 0
	justEnteredPerson = False
	peopleEvents = 0

	#Relays (I got these backwards)
	R1 = 0 #purple
	R2 = 1 #teal
	R3 = 1 #yellow NC R2
	R4 = 1 #blue NC R1

	#for wandering dot
	right = False
	left = False
	up=False
	down=False
	vert=False
	horiz=False
	xBig = False
	yBig = False
	same=False
	denom = 0
	xV1 = 5
	yV1 = 11
	c1 = 15

	try:
		while True:
			#update
			currentTime = time.time()

			fingerNum, fingerPos, fingerUpdate, fingers = getFings(fingerThread, fingers)
			#if time.time()-currentTime > 0.0015:
				#print "fingers slow", time.time() - currentTime

			reading, personNearby, ranger, d, toc, button = sensors(senseThread, toc)
			#if time.time()-currentTime > 0.002:
				#print "sensors slow", time.time() - currentTime

		
			'''sensors demo/person switch'''

			#print button
	 
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

			#print demo, person, fingers
			#demo = True

			'''
			denom = ((time.time()-startTime)/100)+1

			print demo, demoEvents, demoEvents/denom
			print fingers, justSawFingers, fingerEvents, fingerEvents/denom
			print person, peopleEvents, peopleEvents/denom
			'''


			modes = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
			numModes = len(modes)

			skipList = [3,11,13,15,16,17,18]
			#skipList = [15,3]

			agro = [3,18]

			heart = [10,15]

			calm = [0,14,12.9]

			alien = [12,4]

			water = [6,1]		

			favList = [0,5,8]

			boring = [2]

			happy = False
			angry = False
			bored = False

			if happy: modes = favList+water+calm+heart
			if angry: modes = favList+agro+alien+water
			if bored: modes = water+alien
		
			#update mode
			modeDelay = 20
			if (currentTime - lastTimeMode) > modeDelay:
				if oneMode: mode = thisMode;
				if not oneMode: mode += 1;
				if mode > maxMode: mode = 0
				lastTimeMode = currentTime
				selector = random.randrange(numModes)


				if not oneMode:
					if selector not in skipList:
						mode = modes[selector]
					if selector in skipList:
						selector = random.randrange(len(favList))
						mode = favList[selector]
		
		
				print modes, numModes, selector, mode

			def diags(xVal, yVal,color, newSim):
				for i,valI in enumerate(xVal):
					for j, valJ in enumerate(yVal):
						thisMatrix = dot(yVal[j],xVal[i],color)
						newSim = where(newSim != 0, newSim, thisMatrix)
				return newSim
		
			#delay = delaySave
			if (currentTime - lastTimeDelay) > delaySave:
				lastTimeDelay = currentTime

				'''if person nearby'''
				if not person: justEnteredPerson = True
				if person:
					delaySave = personDelay
					if justEnteredPerson:
						peopleEvents = peopleEvents + 1
						justEnteredPerson = False
					fade = True
					sendSim = dot(0,0,0)

					if d >= 3 and d > 0:
						xVal = [5]
						yVal = [11]
						color = 15
						thisMatrix = diags(xVal, yVal,color, sendSim)
						sendSim = where(sendSim != 0, sendSim, thisMatrix)
				
					if d >= 3 and d > 0:
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
				#mode = 6
				if not demo: justEnteredDemo = True
				if demo:
					delaySave = demoDelay
				
					if justEnteredDemo:
						demoEvents = demoEvents + 1
						justEnteredDemo = False

					#dichro
					if mode == 0: 
						sendSim,count = patternZero(sendSim,count)
						fade = True
						#delay = 1
					#2 chevrons purp blue
					if mode == 1: 
						sendSim, simulator2 = patternOne(simulator2,86,66)
					#2 chevrons bl yl
					if mode == 2: sendSim, simulator2 = patternTwo(simulator2,36,66)
					#2 chevrons alt fast red blue
					if mode == 3: sendSim, simulator2 = patternThree(simulator2,15,65)
					#green stripe on blue
					if mode == 4: 
						sendSim, simulator2,count = patternFour(simulator2,32,65,count)
						fade = False
					#yellow with blue chevron
					if mode == 5: 
						sendSim, simulator2 = patternFive(simulator2,54,64,34,2)
						fade = False
					#very blue
					if mode == 6: sendSim, simulator2 = patternSix(simulator2,33,66)
					#very purp
					if mode == 12: sendSim, simulator2 = patternSix(simulator2,33,76)
					#blue red chevron
					if mode == 7: sendSim, simulator2,count = patternFour(simulator2,24,65,count)
					#2 chevrons peach and purp
					if mode == 8: sendSim, simulator2 = patternEight(simulator2,76,26)
				
					'''
					#pink waves
					if mode == 9: 
						newSim, state, switch = patternNine(state,34, switch)
					'''
					#pink waves				
					if mode == 13:sendSim, simulator6, state2 = patternTen(simulator6,state2,44)
					#love 11 pink wiggles with heart
					if mode == 11:
						sendSim, simulator6, state2 = patternTen(simulator6,state2,44)
						sendSim =  where(simulator5!=0,simulator5,sendSim)
					#yellow with heart				
					if mode == 18:
						sendSim, state, switch = patternNine(state,34, switch)
						sendSim =  where(simulator5!=0,simulator5,sendSim)
					if mode == 10:
						sendSim, simulator6, state2 = patternTen(simulator6,state2,44)
						sendSim =  where(simulator5==0,simulator5,sendSim)
					#specular 				
					if mode == 14:
						sendSim,count = patternZero(sendSim,count)
						fade = True
						#delay = 1
					if mode == 9:
						sendSim,count = patternZero(sendSim,count)
						fade = True
						#delay = 1
					#red heart				
					if mode == 15:
						fade = True
						sendSim = simulator5
					#peach wiggle 
					if mode == 16:
						sendSim, simulator7, state2 = patternTen(simulator7,state2,56)
						simulator8 = roll(simulator8,-1,0)
						sendSim =  where(simulator8!=0,simulator8,sendSim)
					#yellow with blue chevron
					if mode == 17: 
						sendSim, simulator2 = patternFive(simulator2,56,66,14)
						fade = False

					#yellow with blue chevron
					if mode == 19: 
						delaySave = demoDelay
						sendSim, simulator2 = patternFive(simulator2,54,64,34,2)
						fade = True
					#move one dot around slowly				
					if mode == 20:
						delaySave = wanderDelay	
						fade = True				

						sendSim = dot(0,0,0)
						thisMatrix = dot(0, 0, 0)
						thisMatrix1 = dot(0, 0, 0)
						thisMatrix0 = dot(0, 0, 0)

						clrz = [16,26,36,46,56,66,76,86]
					
						if not horiz and not vert:
							xV2 = random.randrange(0,10)
							yV2 = random.randrange(0,21)
							c2 = clrz[random.randrange(0,7)]
					
						if horiz or vert:
							if right:
								xV2 = xV2 + run
							if left:
								xV2 = xV2 - run
							if up:
								yV2 = yV2 + rise
							if down:
								yV2 = yV2 - rise


						diffX = xV2 - xV1
						diffY = yV2 - yV1

						#print diffX, diffY
						#if X is neg, move right
						#if Y is neg, move up
						#0,0 is bottom left
						if diffX < -1: right=True; left=False; horiz=True
						if diffX > 1: right=False; left=True; horiz=True
						if diffX <= 1 and diffX >= -1: right=False; left=False; horiz=False
						if diffY < -1: up=True; down=False; vert=True
						if diffY > 1: up=False; down=True; vert=True
						if diffY <= 1 and diffY >= -1: up=False; down=False; vert=False
						diffX = abs(diffX); diffY = abs(diffY)

						if diffX > diffY: xBig = True; yBig=False; same=False
						if diffX < diffY: xBig = False; yBig=True; same=False
						if diffX == diffY: xBig = False; yBig=False; same=True

						if xBig or same: denom = diffX
						if yBig: denom = diffY

						if denom != 0:
							rise = diffY*1.0/denom
							run = diffX*1.0/denom
						if denom == 0:
							rise = 0; run = 0

						#print diffX, diffY, right, left, horiz, up, down, vert, rise, run, denom
						thisMatrix1=dot(yV1,xV1,c1)
						thisMatrix2=dot(yV2, xV2,c2)

						thisMatrix = where(thisMatrix1 != 0, thisMatrix1, thisMatrix2)

						sendSim = where(sendSim != 0, sendSim, thisMatrix)

					

				'''enter fingers mode'''
				#make this random if time has elapsed
				fmode = 0
				if not fingers: justEnteredFingers = True
				if fingers:
					delaySave = fingerDelay
					if justEnteredFingers:
						fingerEvents = fingerEvents + 1
						justEnteredFingers = False
					fade = False
					justSawFingers = True
					decayTimeStart = time.time()

					if fmode == 0:
						sendSim = dot(0,0,0)	

						#print (fingerPos)
		  
						for index, info in enumerate(fingerPos):
							color = (index*10) + 6
							if info[1] >= 0 and info[0] >= 0:
								if info[0] < 11 and info[1] < 22:
									thisMatrix = dot(info[1],info[0],color)
									sendSim = where(sendSim != 0, sendSim, thisMatrix)
					if fmode == 1:
						LeftFing = fingerPos[1]
						RightFing = fingerPos[6]
						isLeft = False
						isRight = False

						if LeftFing != (-1,-1,-1):
							isLeft = True
							
						if RightFing != (-1,-1,-1):
							isRight = True

						if isLeft and not isRight:
							xV1 = LeftFing[0]
							yV1 = LeftFing[1]
							c1 = 15
						if isRight and not isLeft:
							xV1 = RightFing[0]
							yV1 = RightFing[1]
							c1 = 25
						if isRight and isLeft:
							xV1 = RightFing[0]
							yV1 = RightFing[1]
							c1 = 25

						
						delaySave = wanderDelay	
						fade = True				

						sendSim = dot(0,0,0)
						thisMatrix = dot(0, 0, 0)
						thisMatrix1 = dot(0, 0, 0)
						thisMatrix0 = dot(0, 0, 0)

						
						clrz = [16,26,36,46,56,66,76,86]
					
						if not horiz and not vert:
							xV2 = random.randrange(0,10)
							yV2 = random.randrange(0,21)
							c2 = clrz[random.randrange(0,7)]
					
						if horiz or vert:
							if right:
								xV2 = xV2 + run
							if left:
								xV2 = xV2 - run
							if up:
								yV2 = yV2 + rise
							if down:
								yV2 = yV2 - rise


						diffX = xV2 - xV1
						diffY = yV2 - yV1

						#print diffX, diffY
						#if X is neg, move right
						#if Y is neg, move up
						#0,0 is bottom left
						if diffX < -1: right=True; left=False; horiz=True
						if diffX > 1: right=False; left=True; horiz=True
						if diffX <= 1 and diffX >= -1: right=False; left=False; horiz=False
						if diffY < -1: up=True; down=False; vert=True
						if diffY > 1: up=False; down=True; vert=True
						if diffY <= 1 and diffY >= -1: up=False; down=False; vert=False
						diffX = abs(diffX); diffY = abs(diffY)

						if diffX > diffY: xBig = True; yBig=False; same=False
						if diffX < diffY: xBig = False; yBig=True; same=False
						if diffX == diffY: xBig = False; yBig=False; same=True

						if xBig or same: denom = diffX
						if yBig: denom = diffY

						if denom != 0:
							rise = diffY*1.0/denom
							run = diffX*1.0/denom
						if denom == 0:
							rise = 0; run = 0

						#print diffX, diffY, right, left, horiz, up, down, vert, rise, run, denom
						thisMatrix1=dot(yV1,xV1,c1)
						thisMatrix2=dot(yV2, xV2,c2)

						thisMatrix = where(thisMatrix1 != 0, thisMatrix1, thisMatrix2)

						sendSim = where(sendSim != 0, sendSim, thisMatrix)
					fingerNum = 5

				#if fingers are lost for a short time
				if justSawFingers == True:
					delaySave = 0.1
					sendSim = roll(sendSim,-1,0)
					fade = True
					if currentTime-decayTimeStart > 10:
						justSawFingers = False
						fingers = False

			#show
			if fade:
				step = 0.5
				#if not justSawFingers:
				#	step = 0.7
				#if justSawFingers:
				#	step = 2.5
				if bright == 0: sign = 1; justSawFingers = False; count = count+12;	
				bright = bright+(step*sign)
				if bright >= 255-step+1:
					sign = -1
				sendIt(sendSim, fingerNum, ser, bright, R1, R2, R3, R4)

			if not fade:
				sendIt(sendSim, fingerNum, ser, 255, R1, R2, R3, R4)
	except (KeyboardInterrupt, SystemExit):

		#end threads
		fingerThread.join(0)
		senseThread.join(0)
