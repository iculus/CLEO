#!/usr/bin/python

#this program starts the leap class and gets and calibrates finger measurments 
#the calibrated measurements are structured and sent over ZM0 in the onFrame event
#the program makes certain that only one instance of leapd is running
#this is the main leap program

#this relies on launchLeapd, sockets, procCtl, and calibrate

import os, signal, sys, inspect, thread, time, random, struct
		
LIB_DIR = "/home/admin/Desktop/LeapDeveloperKit_2.3.1+31549_linux/LeapSDK/lib"
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '/x64'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, LIB_DIR + arch_dir)))
sys.path.insert(0, LIB_DIR)
#sys.path.insert(0,'/home/admin/Desktop/cuttlefishLights/leapController/')
sys.path.insert(0,'/home/admin/CLEO/Leap')
sys.path.insert(0,'/home/admin/CLEO/Sockets')
sys.path.insert(0,'/home/admin/CLEO/Setup')
sys.path.insert(0,'/usr/lib/python2.7')

import Leap 

#from patterns import heart, dot, diagonalLine, chevronLine
#from sercoms import sendIt, setupSerial
from procCtl import setupProcess, killProcess, set_procname
from calibrate import returnCalibratedPosition

from numpy import interp, zeros, chararray, reshape, append, array, roll

from sockets import *
from setup import *

# setup area #
#physical object dimensions
if thisCLEO == "cleo01":
	LeapRowMin = -150
	LeapRowMax = 150
	M0RowMin = 10
	M0RowMax = 0
	LeapColMin = 50
	LeapColMax = 400
	M0ColMin = 0
	M0ColMax = 21
	LeapZMin = -50
	LeapZMax = 50
	M0ZMin = 100
	M0ZMax = 0

pixelRow = pixelCol = 0
count = 0
maxCount = 22

#fingerListLeft = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
#fingerListRight = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]

def resetFings():
	allFings = [(-1,-1,-1),(-1,-1,-1),(-1,-1,-1),(-1,-1,-1),(-1,-1,-1),(-1,-1,-1),(-1,-1,-1),(-1,-1,-1),(-1,-1,-1),(-1,-1,-1)]
	return allFings
	
def resetSim():
	return zeros([M0ColMax,M0RowMin])
def resetSim2():
	c = chararray([M0ColMax,M0RowMin])
	c[:] = '.'
	return c
	
class SampleListener(Leap.Listener):

	def on_connect(self,controller):
		print "connected"

	def on_device_change(self, controller):
		print "Device change"
	
	def on_device_failure(self, controller):
		print "Failure"

	def on_diagnostic_event(self, controller):
		print "Diagnositc Event"

	def on_disconnect(self, controller):
		# Note: not dispatched when running in a debugger.
		print "Disconnected"		
	
	def on_exit(self, controller):
		killProcess('leapd')
		print "Exited"

	def on_focus_gained(self, controller):
		print "Focused"

	def on_focus_lost(self, controller):
		print "Unfocused"

	def on_init(self, controller):
		print "Initialized"
		print "starting Leap Service"
		setupProcess("leapd", "sudo leapd &") 

	def on_service_change(self, controller):
		print "change", 

	def on_service_disconnect(self, controller):
		print "Lost Connection"
		print "starting Leap Service"
		setupProcess("leapd", "sudo leapd &")
	
	def on_service_connect(self, controller):
		print "Connection Gained"
		
	
	def on_frame(self, controller):

		frame = controller.frame() 
		extended_fingers = frame.fingers.extended()
		hands = frame.hands
		
		numFing = len(extended_fingers)
				
		#returns a list of all finger tip positions 
		allFings = resetFings()
		for f in extended_fingers:
			thisRow = returnCalibratedPosition(
				f.stabilized_tip_position[0],LeapRowMin,LeapRowMax,M0RowMin,M0RowMax)
			thisCol = returnCalibratedPosition(
				f.stabilized_tip_position[1],LeapColMin,LeapColMax,M0ColMin,M0ColMax)
			thisZ = returnCalibratedPosition(
				f.stabilized_tip_position[2],LeapZMin,LeapZMax,M0ZMin,M0ZMax)
			
			if thisCLEO == "cleo01":
				thisCol = M0ColMax - thisCol			

			if f.hand.is_left:
				allFings[f.type] = (thisRow,thisCol,thisZ)
			if f.hand.is_right:
				allFings[f.type+5] = (thisRow,thisCol,thisZ)	
	
		#send message here on ZM0
		topic = 10001
		messagedata = ":" + str(allFings) + ":" + str(numFing)
		fingerSocket.send("%d %s" % (topic, messagedata))		

def main():
	#set up socket for sending on ZM0
	port = "5556"
	global fingerSocket
	fingerSocket = init(port)

	#init serial
	#global ser
	#ser = setupSerial()
	set_procname("crystalz-sense")

	#init leap
	listener = SampleListener()
	controller = Leap.Controller()
	controller.add_listener(listener)

	# Keep this process running until Enter is pressed
	while True: 
		pass

if __name__ == "__main__":
	killProcess("leapd")
	main()
