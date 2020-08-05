import sys


default_run_time = 20 #minutes

#Principal commands
commands = {'turn on' : 1, 'turn off' : 0, 'check' : 2, 'report' : 3, 'clear command' : 4}

#Alternative ways of expressing principal commands
alt_commands = {'start' : 1, 'stop' : 0, 'delete command' : 4}


#principal controlled devices
devices = {'lights' : 1}

#Alternative ways of naming controlled devices
alt_devices = {'illumination' : 1}



#Updating the dictionaries
commands.update(alt_commands)
devices.update(alt_devices)


#get command message
message_file = 'command.txt'
message = open(message_file, 'r').read()

#compute cmmand
message = message.lower()
print('Received command: ', message)

split_message = message.split()


command = -1
for key in commands:
	if all(item in split_message for item in key.split()):
		command = commands.get(key)

device = -1
for key in devices:
	if all(item in split_message for item in key.split()):
		device = devices.get(key)


#Timing of command
start_delay = 0
run_time = default_run_time * 60

if 'in' in split_message:
	i = split_message.index('in')

	val = int(split_message[i+1])

	unit = split_message[i+2]

	if 'min' in unit:
		start_delay = val * 60

	elif 'hour' in unit:
		start_delay = val * 60 * 60
	else:
		pass

if 'for' in split_message:
	i = split_message.index('for')

	val = int(split_message[i+1])

	unit = split_message[i+2]

	if 'min' in unit:
		run_time = val * 60

	elif 'hour' in unit:
		run_time = val * 60 * 60
	else:
		pass


import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)

def turn_on():
    print('Turned on:', time.time())

def turn_off():
	print('Turned off:', time.time())



if command != -1 and device != -1:
	print('Command: ', command)
	print('Device: ', device)

	print('To start in ',start_delay / 60, ' sec. and finish in ', (start_delay + run_time) / 60, ' sec.')

	scheduler.enter(start_delay / 60,1, turn_on)
	scheduler.enter((start_delay + run_time) / 60, 1, turn_off)

	scheduler.run()



