#!/usr/bin/python

import os, signal, sys, inspect, thread, time, random, struct, time
from numpy import interp, zeros, chararray, reshape, append, array, roll, fliplr, where, add, flipud, uintc, rot90

#sys.path.insert(0,'/home/admin/Desktop/cuttlefishLights/leapController/')
sys.path.insert(0,'/home/admin/CLEO/Leap/')
sys.path.insert(0,'/home/admin/CLEO/Setup/')
#sys.path.insert(0,'/home/admin/CLEO/Sockets/')
sys.path.insert(0,'/usr/lib/python2.7')
#sys.path.insert(0,'/home/admin/CLEO/Utilities/')
import subprocess

from setup import *
from procCtl import setupProcess, set_procname

from patterns import *


import serial, struct, sys
start = chr(255)
end = chr(254)

def startProcess():
	p = subprocess.Popen(['./findDevicePath.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="/home/admin/CLEO/Utilities")
	out, err = p.communicate()
	return out

def getPort(device):
	result = startProcess().split('\n')
	for res in result:
		port = "NA"
		err = False
		try:
			dev,name = res.split(' - ')
			if "tty" in res:
				if device in name:
					port = dev
					return port, err
	
		except:
			err = True
	return port, err

def sendIt(sim, numFings, ser, bright, R1, R2, R3, R4):
	sim = flipud(sim)
	toSend = sim.T
	toSend = toSend.reshape(242)

	#add the numfings to the end of the message
	toSend = append(toSend,numFings) 

	#add the brightness to the end of the message
	toSend = append(toSend,bright)

	#add the relaystates end of the message
	toSend = append(toSend,R1)
	toSend = append(toSend,R2)
	toSend = append(toSend,R3)
	toSend = append(toSend,R4)

	#build struct and send messa
	message = start+struct.pack("<248B", *toSend)+end
	ser.write(message)
	ser.flush()
	#time.sleep(1./120)

	#read incoming message
	inp = ser.read(ser.in_waiting)
	
    	try:vals = str(inp).split('-')
	except: vals = "error"
	#ser.flushInput()
	#ser.flushOutput()	
	return vals
	#print(vals)
    	

def setupSerial(TYPE, br=9600, to = 0):
	FeatherPort,FPErr = getPort(TYPE)
	
	if FPErr: 
		print "Port Error", TYPE, FPErr

	serFeather = serial.Serial(port = str(FeatherPort.strip(' ')), baudrate = br, timeout = 0, xonxoff = True, rtscts = True, dsrdtr=True)

	try:
		if(serFeather.isOpen() != False):
			print TYPE, 'Serial Port Open'
		if(serFeather.isOpen() == False):
			ser.open()
			print TYPE, 'is not open'
	except IOError: # if port is already opened, close it and open it again and print message
		print 'error'
		serFeather.close()
		serFeather.open()
	return serFeather


if __name__ == "__main__":
	set_procname("crystalz-lights")
	ser = setupSerial(LEDComputer, 9600, 0)

	#timers
	startTime = currentTime = lastTimeDelay = lastTimeMode = decayTimeStart = time.time()
	delaySave = 0.05


	#for the send
	bright = 0
	fade = True

	#for simulators
	sendSim = dot(0,0,0)

	#Relays (I got these backwards)
	R1 = 0 #purple
	R2 = 1 #teal
	R3 = 1 #yellow NC R2
	R4 = 1 #blue NC R1


	endTime = currentTime = writeTime = time.time()
	count = 0
	fingerNum = 5

	simulator7 = makeSaw(26)
	simulator8 = heart(83)
	state2=0
	
	simulator2 = chevronLine(False)


	try:
		while True:
			currentTime = time.time()
				
			#delay = delaySave
			if (currentTime - lastTimeDelay) > delaySave:
				lastTimeDelay = currentTime

				#sendSim = diagonalLine()
	
				sendSim, simulator7, state2 = patternTen(simulator7,state2,56)
				simulator8 = roll(simulator8,-1,0)
				sendSim =  where(simulator8!=0,simulator8,sendSim)
				
				#sendSim, simulator2 = patternOne(simulator2,86,66)
				
				sendSim = uintc(sendSim)
			


			#show
			fade = True
			if fade:
				step = 0.5
				if bright == 0: sign = 1; justSawFingers = False; count = count+12;	
				bright = bright+(step*sign)
				if bright >= 255-step+1:
					sign = -1
				fromArd = sendIt(sendSim, fingerNum, ser, bright, R1, R2, R3, R4)
				source = "    Fade"

			if not fade:
				bright = 255
				fromArd = sendIt(sendSim, fingerNum, ser, bright, R1, R2, R3, R4)
				source = "Not Fade"

			#print '\nfromPC\n', sendSim
			print bright, source, fromArd, len(fromArd)
			
			

			tft = []	
			name = "*"	
			fig = 0	
			bri = 0
			rel1 = 0
			nd = 0
			nd2 = 0

			try: 
				for ndx,val in enumerate(fromArd):
					if ndx == 0: name = val
					if ndx >= 1 and ndx <= 242 and val != '\r\n': 
						try: 
							#print ndx, val, ord(val),
							tft.append(ord(val))
						except: print ndx, "error"
					if ndx == 243: 
						try: fig = ord(val)
						except: fig = 'x'
					if ndx == 244: 
						try: bri = ord(val)
						except: bri = 'x'
					if ndx == 245: 
						try: rel1 = ord(val)
						except: rel1 = 'x'
					if ndx == 246: 
						try: rel2 = ord(val)
						except: rel2 = 'x'
					if ndx == 247: 
						try: rel3 = ord(val)
						except: rel3 = 'x'
					if ndx == 248: 
						try: rel4 = ord(val)
						except: rel4 = 'x'
					if ndx == 249: 
						try: nd = ord(val)
						except: nd = 'x'
					if ndx == 250: 
						try: nd2 = val
						except: nd2 = 'x'
					#if val == '\r\n': print ndx, 'good'

				#print tft
				#print len(tft)

				if len(tft) == 242: print rot90(reshape(tft,[11,22])),'\n', name, fig, bri, rel1, rel2, rel3, rel4, nd, repr(nd2)
			except: print "corruption error"
			

	except (KeyboardInterrupt, SystemExit):
		pass
