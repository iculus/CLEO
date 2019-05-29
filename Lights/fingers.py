def getFings(fingerThread, fingers):
	'''get fingers info'''			
	fingerUpdate = False
	fingerTopic = 0
	fingerPos = 0,0
	fingerNum = 0
 	
	#digest the finger stream
	fingInfo = str(fingerThread).replace(" ", "")
	if fingInfo != "NONE": 
		fingerTopic, fingerPos, fingerNum = fingInfo.split(":")
		fingerPos = fingerPos.strip('[').strip(']').split('),(')

	if len(fingerPos) > 2:
		for index,fing in enumerate(fingerPos):
			x,y,z = fing.strip('(').strip(')').split(',')
			thisFing = (int(x), int(y), int(z))
			fingerPos[index] = thisFing
		fingerUpdate = True
		negOneCount = 0
		for f in fingerPos:
			for ff in f:
				if ff == -1:
					negOneCount = negOneCount + 1
		if negOneCount == 30: #because 10 fingers X 3 axis
			fingers = False #all values are false

	fingerNum = int(fingerNum)
	return fingerNum, fingerPos, fingerUpdate, fingers
