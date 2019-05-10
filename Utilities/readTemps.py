#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, time
sys.path.insert(1,'/usr/lib/python2.7')
import subprocess

from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
from ascii_graph.colordata import hcolor

def getTemps():
	temps = []
	p = subprocess.Popen(['sensors'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")
	rc = p.returncode

	outputs = output.split('\n')

	for i in outputs:
		if i.split(' ')[0] =="Core":
			val = i.split()[2].strip('+').strip('C').strip('°')
			temps.append( float(val) )
	return temps

timeStart = time.time()

graph = Pyasciigraph(
	line_length=55,
	min_graph_length=50,
	separator_length=4,
	multivalue=False,
	human_readable='si',
	graphsymbol='*',
	float_format='{0:,.2f}',
	force_max_value=90)
pattern = [Gre, Yel, Red]
thresholds = {
	51:  Gre, 60: Blu, 65: Yel, 70: Red,
}

if __name__ == "__main__":
	while True:
		timeNow = time.time()
		if timeNow-timeStart > 1:
			temps = getTemps()
			data = [('core1',temps[0]),('core2',temps[1]),('core3',temps[2]),('core4',temps[3])]
			data = hcolor(data, thresholds)			
			#data = vcolor(data, pattern)
			timeStart = time.time()
			subprocess.call("clear", shell=True)
			for line in  graph.graph('Temps', data):
			    print(line)
