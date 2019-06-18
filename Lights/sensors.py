def map(x, in_min, in_max, out_min, out_max):
	return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

		
def sensors(senseThread, timeoutCounter):

	'''get the sensors data'''
	
	ranger = 0
	lux = 0
	white = 0
	als = 0
	reading = False
	distanceMin = 10
	distanceMax = 1200
	personNearby = False
	d = 0
	header="err"
	message = (0,0,0,0)

	#print str(senseThread)
	#clean the thread update
	if str(senseThread) != "NONE":
		try:
			header, message = str(senseThread).replace('\r', '').replace(' ','').split(':')
			#print(header, message)
			try:
				ranger, lux, white, als = message.split(',') 
			except: pass
		except: pass

		#print ranger, lux, white, als
		#topic, ranger = str(senseThread).replace(" ", "").split(":")
	
	#map ranger to steps
	rangerMin = 0
	rangerMax = 7

	ranger = int(ranger)

	if ranger > 8180 and ranger < 8200:
		reading = False

	elif ranger <= distanceMax:
		reading = True	
		timeoutCounter = 0	
		d = map(ranger, distanceMin, distanceMax, rangerMin, rangerMax)

	#print d, ranger, reading
	
	#check for people
	if d > 1 and d < 7 and reading == True:
		personNearby = True
	elif d <= 1 or d >= 7 and reading == True:
		personNearby = False
	if reading == False:
		timeoutCounter = timeoutCounter + 1
		if timeoutCounter > 20:
			timeoutCounter = 0
			personNearby = False
	#if reading == True:
	return reading, personNearby, ranger, d, timeoutCounter
