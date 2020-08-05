#https://github.com/carpedm20/fbchat

import fbchat
import time

import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setup(2, GPIO.OUT, initial=GPIO.HIGH)   # Set pin 8 to be an output pin and set initial value to low (off)


email = "tdrvlad@gmail.com"
password = "12345678901234567890"

command_password = "please"

log_file = "Log.txt"

session = fbchat.Session.login(email, password)
listener = fbchat.Listener(session=session, chat_on=False, foreground=False)

verified_users = []

on_command = 'Turn on Lights'
off_command = 'Turn off lights'

on_command.lower().split()
off_command.lower().split()

print(on_command)



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
				
				message.lower().split()

				if all(item in on_command for item in message) or all(item in message for item in on_command):
 			
					thread.send_text('Turning on lights')
					GPIO.output(2, GPIO.LOW)
				
				elif all(item in off_command for item in message) or all(item in message for item in off_command):
					thread.send_text('Turning off lights')
					GPIO.output(2, GPIO.HIGH)
				else:
					thread.send_text('Waiting for command')
					time.sleep(15)



			







