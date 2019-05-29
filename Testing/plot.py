


'''
0 timed print 0
1  BAUD : 4800 timeout : 0 time 300
2   unfiltered
3    AVGTime : 19.894275 AVGDrop : 8 NUM : 8
4    time : 0.338300,0.010500,0.051600,72.536800,0.045600,2.491000,0.013000,83.667400,
5    drops : 1,1,14,13,10,16,2,13,
'''


switch = False

pos = 0
viewer = False

dataHolder = []

with open("saved") as fl:

	for linenum, line in enumerate(fl):
		line = line.strip("\n")
		if "print" in line:
			switch = True
		if "filtered" in line and "unfiltered" not in line:
			switch = False
		if viewer: print switch, linenum,
		if not switch:
			if viewer: print '\r'
			counter = 0
		if switch:
			if viewer: print counter, line
			dataHolder.append(line)

print '\n'

start = 0
change = 5
end = start + change

filt = 20

whole = []
while end <= len(dataHolder):
	temp = []
	for i in dataHolder[start:end+1]:
		temp.append( i )
	whole.append( temp )
	start = end +1
	end = end + change +1


bauds = []
drops = []
dropsFilt = []

for i in whole:
	row1 = i[0].split(' ')
	row2 = i[1].split(' ')
	row3 = i[2].split(' ')
	row4 = i[3].split(' ')
	row5 = i[4].split(' ')
	row6 = i[5].split(' ')

	'''
	['', '', '', 'AVGTime', ':', '47.864950', 'AVGDrop', ':', '1', 'NUM', ':', '2']
	['', '', '', 'time', ':', '1.573200,94.156700,']
	['', '', '', 'drops', ':', '1,2,']
	'''

	name = row1[2]
	baud = row2[3]
	timeout = row2[6]
	window = row2[8]

	avgTime = row4[5]
	avgDrop = row4[8]

	timeListTemp = row5[5].split(',')[:-1]
	dropListTemp = row6[5].split(',')[:-1]

	timeList = []
	dropList = []
	
	for jdex, j in enumerate(timeListTemp):
		timeList.append(float(j))
		dropList.append(int(dropListTemp[jdex]))

	filtTimeList = []
	filtDropList = []

	for indx, vals in enumerate(dropList):
		if int(vals) >= int(filt):
			filtDropList.append(int(vals))
			filtTimeList.append(float(timeList[indx]))

	numDrops = len(dropList)
	numDropsFilt = len(filtDropList)
		

	print name, baud, timeout, window
	print avgTime, avgDrop
	print timeList
	print dropList
	print filtTimeList
	print filtDropList
	print numDrops
	print numDropsFilt
	print '\n'

	bauds.append(baud)
	drops.append(numDrops)
	dropsFilt.append(numDropsFilt)

import numpy as np
import matplotlib.pyplot as plt

# data to plot
n_groups = len(drops)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, drops, bar_width,
alpha=opacity,
color='b',
label='Drops W/O')

rects2 = plt.bar(index + bar_width, dropsFilt, bar_width,
alpha=opacity,
color='g',
label='Drops W/')

plt.xlabel('Baud Rate')
plt.ylabel('Num Drops')
plt.title('Eval CLEO Dropped Messages')
plt.xticks(index + bar_width, bauds, rotation='vertical')
plt.legend()

plt.savefig('graph.png', bbox_inches='tight')

plt.tight_layout()
plt.show()


