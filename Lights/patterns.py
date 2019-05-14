from numpy import interp, zeros, chararray, reshape, append, array, roll, where, fliplr, add, vstack, full, delete

def heart(color):
	x = color
	return array([	[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,x,x,0,0,0,x,x,0,0],
			[0,x,0,0,x,0,x,0,0,x,0],
			[x,0,0,0,0,x,0,0,0,0,x],
			[x,0,0,0,0,0,0,0,0,0,x],
			[x,0,0,0,0,0,0,0,0,0,x],
			[0,x,0,0,0,0,0,0,0,x,0],
			[0,0,x,0,0,0,0,0,x,0,0],
			[0,0,0,x,0,0,0,x,0,0,0],
			[0,0,0,0,x,0,x,0,0,0,0],
			[0,0,0,0,0,x,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],	
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0]	])

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

def diagonalLine():
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

def patternAdd(arrayToAdd,count):
	addArray = array([[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],	
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0],
			[0,0,0,0,0,2,0,0,0,0,0]	])
	addArray = roll(addArray,count,1)

	return add(addArray,arrayToAdd)

def patternOne (start,c1,c2):
	#flips and copies
	copy=fliplr(start)
	start2=roll(start,-1,1)
	start3=roll(start,-2,1)
	copy2=roll(copy,1,1)
	copy3=roll(copy,2,1)

	#sets color
	start=where(start == 0, start,c1)
	start2=where(start2 == 0, start2,c1-1)
	start3=where(start3 == 0, start3,c1-2)
	copy=where(copy == 0, copy,c2)
	copy2=where(copy2 == 0, copy2,c2-1)
	copy3=where(copy3 == 0, copy3,c2-2)

	#merges
	newSim=where(start !=0, start,copy)
	newSim=where(newSim !=0,newSim,start2)
	newSim=where(newSim !=0,newSim,start3)
	newSim=where(newSim !=0,newSim,copy2)
	newSim=where(newSim !=0,newSim,copy3)
	
	#moves
	start=roll(start, 1,1)
	
	return newSim, start

def patternTwo (start,c1,c2):
	#flips and copies
	copy=fliplr(start)

	#sets color
	start=where(start == 0, start,c1)
	copy=where(copy == 0, start,c2)

	#merges
	newSim=where(start != 0, start,copy)
	
	#moves
	start=roll(start, 1,1)
	
	return newSim, start

def patternThree (start,c1,c2):
	#flips and copies
	copy=fliplr(start)

	#sets color
	start=where(start == 0, start,c1)
	copy=where(copy == 0, copy,c2)

	#merges
	newSim=where(start != 0, start,copy)
	
	#moves
	start=roll(start, 1,1)
	
	return newSim, copy

def patternFour (start,c1,c2,count=0):
	#flips and copies
	copy=fliplr(start)

	#sets color
	start=where(start == 0, start,c1)
	copy=where(copy == 0, start,c2)

	#merges
	newSim=where(start != 0, start,copy)
	
	#moves
	start=roll(start, 1,1)

	newSim = patternAdd(newSim,count*count)
	
	#can move it here
	count=count
	
	return newSim, start,count

def patternFive (start,c1=54,c2=64, c3=34, x=2):
	#flips and copies
	copy=fliplr(start)

	#sets color
	start=where(start == 0, start,c1)
	copy=where(copy == 0, start,c2)

	#merges
	newSim=where(start != 0, start,copy)
	
	#moves
	start=roll(start, 1,1)

	addArray = array([[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],	
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0],
		[0,0,0,0,0,x,0,0,0,0,0]	])

	#c3=92

	newSim = add(where(newSim != 0,newSim,c3),addArray)
	
	return newSim, start

def patternSix (start,c1,c2):
	#flips and copies
	copy=fliplr(start)

	#sets color
	start=where(start == 0, start,c1)
	copy=where(copy == 0, start,c2)

	#merges
	newSim=where(start != 0, start,copy)
	
	#moves
	start=roll(start, 1,1)

	addArray = array([[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],	
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0],
		[0,0,0,0,0,22,0,0,0,0,0]	])

	newSim2 = add(where(newSim == 0,newSim,newSim),addArray)
	newSim = where(newSim != 0, newSim2,0)
	
	return newSim, start

def patternZero(newSim,count, count2=0):
	#count = count + 1
	#count = count * 2
	if count > 10000000: count = 0
	import random
	#count = random.randrange(12)
	#count2 = random.randrange(12)
	
	#count = count2 =0
	newSim = array([[0,0,0,12,13,14,15,16,0,0,0],
			[0,0,0,22,23,24,25,26,0,0,0],
			[0,0,0,32,33,34,35,36,0,0,0],
			[0,0,0,42,43,44,45,46,0,0,0],
			[0,0,0,52,53,54,55,56,0,0,0],
			[0,0,0,62,63,64,65,66,0,0,0],
			[0,0,0,72,73,74,75,76,0,0,0],
			[0,0,0,82,83,84,85,86,0,0,0],
			[0,0,0,92,93,94,95,96,0,0,0],
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
			[0,0,0,0,0,0,0,0,0,0,0]])

	
	newSim = roll(newSim,count,1)
	newSim = roll(newSim,count,0)
	return newSim, count

def patternEight (start,c1,c2):

	oneLine = [0,0,0,1,1,2,1,1,0,0,0]
	new = array(oneLine)
	for i in range(22-1):
		new = vstack([new,oneLine])

	oneLine2 = [0,0,0,-1,-1,-2,-1,-1,0,-0,0]
	new2 = array(oneLine2)
	for i in range(22-1):
		new2 = vstack([new2,oneLine2])

	#flips and copies
	copy=fliplr(start)
	
	#sets color
	start=where(start == 0, start,c1)
	copy=where(copy == 0, start,c2)

	start2 = add(where(start==0,start,start),new)	
	start = where(start != 0, start2, 0)

	copy2 = add(where(copy==0,copy,copy),new2)	
	copy = where(copy != 0, copy2, 0)

	#merges
	newSim=where(start != 0, start,copy)
	
	#moves
	start=roll(start, 1,1)
	
	return newSim, start


minColorInt = 2
maxColorInt = 6

def setBrightness(colorVal,brightness):
	if brightness < minColorInt: brightness = minColorInt
	if brightness > maxColorInt: brightness = maxColorInt

	colorInt = colorVal%10
	colorDec = colorVal - colorInt
	colorVal = colorDec+brightness
	
	return colorVal

def patternNine (state, c1, switch):
	if state < minColorInt: state = minColorInt
	clean = dot(0,0,0)

	c1 = setBrightness(c1,state)
	
	newSim = clean
	newSim = where(clean == 0, c1,0)
	
	state = state+(1*switch)
	if state == minColorInt: switch = 1
	if state == maxColorInt: switch = -1
	if state > maxColorInt: state = minColorInt

	return newSim, state, switch

rows = 22

def makeSaw(c1):
	new = full(11,c1)
	
	k = 0
	while k <= rows-1:
		for i in range (maxColorInt-minColorInt+1):
			if k <= rows-1:
				c1 = setBrightness(c1,i+minColorInt)
				row = full(11,c1)
				new =vstack([new,row])
				k += 1
			else: pass
		for j in range (maxColorInt-minColorInt-1):
			if k <= rows-1:
				c1 = setBrightness(c1,maxColorInt-1 - j)
				row = full(11,c1)
				new =vstack([new,row])
				k += 1
			else: pass
	new = delete(new, (0), axis=0)
	return new

def patternTen(start, state,c1):
	
	start = roll(start,-1,0)
	
	return start, start, state
