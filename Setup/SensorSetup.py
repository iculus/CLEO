#!/usr/bin/python


import subprocess, sys, serial
sys.path.insert(0,'/home/admin/CLEO/Setup/')

from setup import *
import serial, struct, sys
from numpy import interp, zeros, chararray, reshape, append, array, roll
from time import sleep

start = chr(255)
end = chr(254)

def readSerialPort(ser):
	for line in ser:
		return line

def readData(ser):
    buffer = ""
    while True:
        oneByte = ser.read(1)
        if oneByte == b"\n":    #method should returns bytes
            return buffer
        else:
            buffer += oneByte.decode("ascii")

def startProcess():
	p = subprocess.Popen(['./findDevicePath.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="/home/admin/CLEO/Utilities")
	out, err = p.communicate()
	return out

def checkLSUSB():
	p = subprocess.Popen(['lsusb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

def sendIt(sim, numFings, ser, bright):
	toSend = sim.T
	toSend = toSend.reshape(242)

	#add the numfings to the end of the message
	toSend = append(toSend,numFings) 

	#add the brightness to the end of the message
	toSend = append(toSend,bright)
	#print(toSend)

	#build struct and send messa
	message = start+struct.pack("<244B", *toSend)+end
	ser.write(message)

	#read incoming message
	inp = ser.readline()
    	vals = str(inp.decode("utf-8")).split(',')
	print(vals)
    	#sleep(1./120)

def setupSerial(TYPE):
	FeatherPort,FPErr = getPort(TYPE)
	
	if FPErr: 
		print "Port Error", TYPE, FPErr

	serFeather = serial.Serial(port = str(FeatherPort.strip(' ')), baudrate = 115200,timeout = 0)

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

	FEATHERLOC = "X"
	LEONARDOLOC = "X"
	HUBLOC = "X"
	LEAPLOC = "X"
	WIFILOC = "X"

	tests = [FEATHERLOC,LEONARDOLOC,HUBLOC,LEAPLOC,WIFILOC]

	testNames = [feather,leonardo,hub,leap,wifi]

	print "\nDevices\n"
	#result = startProcess().split('\n')

	FeatherPort,FPErr = getPort(feather)
	tests[0] = FeatherPort
	print feather, "port -", FeatherPort, "error -" , FPErr

	LeonardoPort,LPErr = getPort(leonardo)
	tests[1] = LeonardoPort
	print leonardo, "port -", LeonardoPort, "error -", LPErr

	lsusb = checkLSUSB().split('\n')

	for thisUSB in lsusb:

		if leap in thisUSB:		
			print "LEAP -", thisUSB
			tests[2] = thisUSB
		if hub in thisUSB:
			print "HUB  -", thisUSB
			tests[3] = thisUSB
		if wifi in thisUSB:
			print "WIFI -", thisUSB
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
