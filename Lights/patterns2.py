from numpy import interp, zeros, chararray, reshape, append, array, roll, where, fliplr, add, vstack, full, delete

def dot(xPos, yPos, Color):
	setArray = array([	[0,0,0,0,0,0,0,0,0,0,0],
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
	setArray[xPos][yPos] = Color
	return setArray

def chevronLine(fill=True):
	if fill: P = 0
	if not fill: P = 7

	return array([	[4,0,0,0,0,0,0,0,0,0,0],
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
			[0,0,0,0,0,0,0,0,0,0,P]	])
