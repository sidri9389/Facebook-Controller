#https://github.com/carpedm20/fbchat

import fbchat
import time
import sys
import RPi.GPIO as GPIO    
import sched


#Lights Relay
lights_relay = 2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setup(lights_relay, GPIO.OUT, initial=GPIO.HIGH)   # Set pin 8 to be an output pin and set initial value to low (off)

def turn_on():
	print('Turned on:', time.time())

	f = open(log_file,"w")
	f.write("Turned lighs on at " + str(time.time()))
	f.close()

	GPIO.output(lights_relay, GPIO.LOW)

def turn_off():
	print('Turned off:', time.time())
	f = open(log_file,"w")
	f.write("Turned lighs off at " + str(time.time()))
	f.close()

	GPIO.output(lights_relay, GPIO.HIGH)


#Bot credentials
email = "tdrvlad@gmail.com"
password = "12345678901234567890"

command_password = "please"

#Definitions

log_file = 'Log.txt'

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


session = fbchat.Session.login(email, password)
listener = fbchat.Listener(session=session, chat_on=False, foreground=False)

verified_users = []


for event in listener.listen():
	if isinstance(event, fbchat.MessageEvent):
		
		if event.author.id != session.user.id:
			
			thread = event.thread

			if event.author not in verified_users:

				thread.send_text("Hello")
				time.sleep(1.5)
				thread.send_text("Type Password")

				time.sleep(7)

				responses = thread.fetch_messages(limit = 1)

				for response in responses:

					print(response.text)
					if command_password == response.text:
							thread.send_text("Access Granted")
							verified_users.append(event.author)

							f = open(log_file,"w")
							f.write("Added user " + str(event.author.id))
							f.close()
					else:
							thread.send_text("Acces Denied")

			else:

				message = event.message.text
				
				#compute command
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


				#Define task scheduler
				scheduler = sched.scheduler(time.time, time.sleep)

				if command != -1 and device != -1:
					print('Command: ', command)
					print('Device: ', device)

					print('To start in ',start_delay / 60, ' sec. and finish in ', (start_delay + run_time) / 60, ' sec.')

					scheduler.enter(start_delay / 60,1, turn_on)
					scheduler.enter((start_delay + run_time) / 60, 1, turn_off)

					scheduler.run()


				if command == 4:
					print('Delete all future events')
					for event in scheduler.queue:
						scheduler.cancel(event)

				if command == 3:
					print('Deelet all future events')
					log = open(log_file, 'r').read()
					thread.send_text(log)
	



			







