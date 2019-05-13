import serial, time, random
import struct
from numpy import interp, zeros, chararray, reshape, append, array, roll

ser = serial.Serial(port = '/dev/ttyACM0', baudrate = 115200,timeout = 0.01)

try:
	print 'its open'
    
	if(ser.isOpen() == False):
		ser.open()
		print 'its not open'
		
except IOError: # if port is already opened, close it and open it again and print message
	print 'error'
	ser.close()
	ser.open()

def readSerialPort():
	for line in ser:
		return line	

while 1:
	while ser.inWaiting() > 0:
		ser.read(1)
	
	start = chr(255)
	end = chr(254)
	
	#x = random.randrange(11) #rows
	#y = random.randrange(22) #columns
	#fing = random.randrange(10) #controls color
	#depth = random.randrange(10) #controls brightness
	
	#x = 11
	#y = 33
	#fing = 55
	#depth = 44
	#xtra = 77
	
	#message = start + struct.pack("<5B", x,y,fing,depth,xtra) + end
	#ser.write(message)
	
	toSend = []
	for i in range(244):
		toSend.append(i)
		
	sim = array([	
			[4,0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0],
			[0,0,2,0,0,0,0,0,0,0,0],
			[0,0,0,3,0,0,0,0,0,0,0],
			[0,0,0,0,4,0,0,0,0,0,0],
			[0,0,0,0,0,5,0,0,0,0,0],
			[0,0,0,0,0,0,6,0,0,0,0],
			[0,0,0,0,0,0,0,7,0,0,0],
			[0,0,0,0,0,0,0,0,8,0,0],
			[0,0,0,0,0,0,0,0,0,9,0],
			[0,0,0,0,0,0,0,0,0,0,10],
			[0,0,0,0,0,0,0,0,0,9,0],
			[0,0,0,0,0,0,0,0,8,0,0],
			[0,0,0,0,0,0,0,7,0,0,0],
			[0,0,0,0,0,0,6,0,0,0,0],
			[0,0,0,0,0,5,0,0,0,0,0],	
			[0,0,0,0,4,0,0,0,0,0,0],
			[0,0,0,3,0,0,0,0,0,0,0],
			[0,0,2,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,0,0,0],
			[9,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0]	])
	
	toSend = sim.T
	toSend = toSend.reshape(242)

	#add the numfings to the end of the message
	numFings = 10
	toSend = append(toSend,numFings) 

	#add the brightness to the end of the message
	bright = 100
	toSend = append(toSend,bright)
	
	message = start + struct.pack("<244B", *toSend) + end
	ser.write(message)

	
	
	print 'writing', int(time.time())
	print readSerialPort()
	time.sleep(1)
