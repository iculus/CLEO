#!/usr/bin/python
# this program takes no input and outputs test patterns to the microcontroller with leds attached

import sys
import time

sys.path.insert(0,'/home/admin/CLEO/Setup/')
sys.path.insert(0,'/home/admin/CLEO/Lights/')

from setup import *
from SensorSetup import *
from numpy import array
from patterns import *

print LEDComputer
print SENSORComputer

print getPort(LEDComputer)
print getPort(SENSORComputer)


#SENSESerial = setupSerial(SENSORComputer)

sendSim = dot(0,0,0)
simulator2 = chevronLine(True)



#other setup
fade = True
bright = 0

testSim = array([	[4,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0],
			[0,0,2,0,0,0,0,0,0,0,0],
			[0,0,0,3,0,0,0,0,0,0,0],
			[0,0,0,0,4,0,0,0,0,0,0],
			[0,0,0,0,0,5,0,0,0,0,0],
			[0,0,0,0,0,0,6,0,0,0,0],
			[0,0,0,0,0,0,0,7,0,0,0],
			[0,0,0,0,0,0,0,0,8,0,0],
			[0,0,0,0,0,0,0,0,0,9,0],
			[0,0,0,0,0,0,0,0,0,0,8],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],	
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0]	])



b = [4800,9600,19200,38400,57600,115200,250000,500000,1000000]
bauds = []
for i in b:
	for j in range(2):
		bauds.append(i)

timecheck = 5*60
print bauds

print "\n\nthis test will take: %d minutes\n\n" % (len(bauds)*timecheck/60)
	

for loop, value in enumerate(bauds):

	remainingTime = (len(bauds)-loop) * (timecheck/60)

	print "\nRemaining Time : %d" % (remainingTime)
	
	go = True
	baud = int(value)
	to = 0

	LEDSerial = setupSerial(LEDComputer, baud, to)

	#timers
	startTime = beginTime = currentTime = lastTimeDelay = lastTimeMode = decayTimeStart = time.time()
	delaySave = 0.05

	#error checkers
	errorDrop = 0
	okay = 0
	totalDrops = 0
	maxDropsList = []
	dSTime = time.time()
	timeDiff = 0
	tList = []
	newDList = []
	newTList = []
	highPass = 30
	allTimes = 0

	#to print
	avgTimeUn = 0
	avgDropUn = 0
	numUn = 0
	avgTimeFIL = 0
	avgDropFIL = 0
	numFIL = 0

	while go:

		#update
		currentTime = time.time()

		delay = delaySave
		if (currentTime - lastTimeDelay) > delay:
			lastTimeDelay = currentTime

			sendSim, simulator2 = patternFive(simulator2,54,64,34,2)
			fade = True

		fingerNum = 3
		timeSend = time.time() % 100000

		#show
		if fade:
			step = 0.5
			if bright == 0: sign = 1; justSawFingers = False; #count = count+12; 
			timeFromFeather = sendIt(sendSim, fingerNum, LEDSerial,bright/60,0,0,0,0)
			bright = bright+(step*sign)
			if bright >= 255-step+1:
				sign = -1
		if not fade:
			timeFromFeather = sendIt(sendSim, fingerNum, LEDSerial,bright/60,0,0,0,0)

		'''testing for dropped messages'''
		okay, totalDrops, maxDropsList, errorDrop, dSTime, timeDiff, tList = checkDrops(
			timeFromFeather, errorDrop, okay, maxDropsList , totalDrops, dSTime, timeDiff, tList, 500)
	
	
		if okay == 1: 
			limit = 5
			rTList = tList[::-1]
			rList = maxDropsList[::-1]

		
			if len(rList) > 0:
				avgTimeUn = sum(rTList)/len(rTList)
				avgDropUn = sum(rList)/len(rList)
				numUn = totalDrops
				print "\n\n\nREAMINING TIME : %f \n" % (remainingTime - (currentTime-beginTime)/60)
				print "UNFILTERED", loop, baud
				print "avg time :", avgTimeUn
				print "avg drop :", avgDropUn
				if len(maxDropsList) <= limit:
					print "\n drops : ", numUn, rList
					print " time : ", rTList, "\n"
				if len(maxDropsList) > limit:
					print "\n drops : ", numUn, rList[0:limit]
					print " time : ", rTList[0:limit], "\n"

			'''filters'''
			#the problem is that the list check loops every time a new item is added to the other list. 
			for indx, val in enumerate(maxDropsList):
				if val <= highPass:
					allTimes = allTimes + tList[indx]
				if val > highPass: 
					allTimes = allTimes + tList[indx]
					newDList.append(val)
					newTList.append(allTimes)
					allTimes = 0

			rNewDList = newDList[::-1]
			rNewTList = newTList[::-1]

		
			if len(rNewTList) > 0:
				avgTimeFIL = sum(rNewTList)/len(rNewTList)
				avgDropFIL = sum(rNewDList)/len(rNewDList)
				numFIL = len(rNewDList)
				print "FILTERED", loop, baud
				print "avg time :", avgTimeFIL
				print "avg drop :", avgDropFIL
				if len(rNewDList) <= limit:
					print "\n drops : ", numFIL, rNewDList
					print " time : ", rNewTList, "\n"
				if len(rNewDList) > limit:
					print "\n drops : ", numFIL, rNewDList[0:limit]
					print " time : ", rNewTList[0:limit], "\n\n"

		#print time.time()-startTime
		if time.time()-startTime >= timecheck:
			f = open ('saved', 'a') 

			print "timed print %d\n" % (loop)
			print " BAUD : %d timeout : %d time %d" % (baud,to,timecheck)
			print "  unfiltered"
			print "   AVGTime : %f AVGDrop : %d NUM : %d" % (avgTimeUn, avgDropUn, numUn)
			print "   times : ", tList
			print "   drops : ", maxDropsList
			print "  filtered"
			print "   AVGTime : %f AVGDrop : %d NUM : %d" % (avgTimeFIL, avgDropFIL, numFIL)
			print "   times : ", newTList
			print "   drops : ", newDList

			f.write( "timed print %d\n" % (loop) )
			f.write( " BAUD : %d timeout : %d time %d\n" % (baud,to,timecheck) ) 
			f.write( "  unfiltered\n" )
			f.write( "   AVGTime : %f AVGDrop : %d NUM : %d\n" % (avgTimeUn, avgDropUn, numUn) )
			f.write( "   time : " )	
			for item in tList:
        			f.write("%f," % item)		
			#f.write( tList )
			f.write( "\n   drops : " )
			for item in maxDropsList:
        			f.write("%d," % item) 
			#f.write( maxDropsList )
			f.write( "\n" )	
			f.write( "  filtered\n" )
			f.write( "   AVGTime : %f AVGDrop : %d NUM : %d\n" % (avgTimeFIL, avgDropFIL, numFIL) )
			f.write( "   time : " )	
			for item in newTList:
        			f.write("%f," % item)		
			#f.write( newTList )
			f.write( "\n   drops : " )
			for item in newDList:
        			f.write("%d," % item) 
			#f.write( newDList )
			f.write( "\n\n\n" )
			f.close()
			go = False
			 
				
	

