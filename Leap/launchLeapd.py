#!/usr/bin/python
from subprocess import Popen, PIPE, check_output
import os, signal

thisPID = []

def do_it2():
	worked = False
	killProcess('leapd')

	#sudo_password = 'admin'
	command = 'leapd'.split()

	p = Popen(['gnome-terminal', '-x', 'sudo', '-S'] + command, stdin=PIPE, stderr=PIPE,universal_newlines=True, shell=False, preexec_fn=os.setpgrp)
	#sudo_prompt = p.communicate(sudo_password + '\n')[1]
	sudo_prompt = p.communicate()[1]

	status = p.wait()

	try:
		thisPID = get_pid('leapd')
		worked = True	
	except:
		worked = False
	return worked

def get_pid(name2):
	try:
		return map(int,check_output(["pidof",name2]).split())	
	except:
		return 'fail'

def killProcess(name):
	runningIDS = get_pid(name)
	if len(runningIDS) > 0 and 'fail' not in runningIDS:
		print 'Kill Leapd Processes'
		for i in runningIDS:
			os.kill(i,signal.SIGTERM)
	if 'fail' in runningIDS:
		print 'all good'


if __name__ == "__main__":
	do_it2()
